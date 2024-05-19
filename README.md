# Task Master: To-Do List Application

## Overview

This project is a simple yet powerful To-Do application built with Flask, a lightweight web framework for Python. The application allows users to register, log in, and manage their personal to-do lists. Each user has their own account and can only access their own tasks, ensuring privacy and security.

## Features

- **User Authentication**: Secure registration and login functionality using hashed passwords.
- **Personalized To-Do Lists**: Each user has their own to-do list, accessible only after logging in.
- **Task Management**: Users can add, update, and delete tasks from their to-do lists.
- **Responsive Design**: Clean and responsive user interface using HTML and CSS.

## Technologies Used

- **Flask**: Web framework for Python.
- **SQLAlchemy**: ORM for database management.
- **Flask-Login**: User session management.
- **WTForms**: Form handling and validation.
- **SQLite**: Lightweight database for storing user and task data.
- **HTML/CSS**: Frontend design and layout.

### Folder Structure

```
flask-todo-app/
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
├── static/
│   └── css/
│       └── main.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── update.html
└── migrations/
```

## Deployment

https://task-master-1-7cc7ba864ad8.herokuapp.com/
