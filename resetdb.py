from app import app, db

def reset():
    try:
        with app.app_context():
            db.drop_all
            db.create_all()
        return 'Database reset successful!'
    except Exception as e:
        return f'An error occurred: {e}'

print(reset())
