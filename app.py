from datetime import datetime
from flask import Flask, current_app, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'ethan'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    todos = db.relationship('Todo', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Todo(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

@app.route('/', methods=['POST', 'GET'])
def index():
    user_todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=user_todos)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_todo = Todo(content=content, user_id=current_user.id)

    try:
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    if task_to_delete:
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that task.'
    else:
        return 'Task not found or you do not have permission to delete it.'

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task_to_update = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    if task_to_update:
        if request.method == "POST":
            task_to_update.content = request.form['content']
            try:
                db.session.commit()
                return redirect("/")
            except:
                return 'There was a problem updating that task.'
        else:
            return render_template('update.html', task=task_to_update)
    else:
        return 'Task not found or you do not have permission to update it.'

@app.route('/reset')
def reset():
    try:
        db.drop_all()
        db.create_all()
        return 'Database reset successful!'
    except Exception as e:
        return f'An error occurred: {e}'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid password. Please try again.')
        else:
            flash('Username not found. Please register or try again.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and not current_user.is_authenticated:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)