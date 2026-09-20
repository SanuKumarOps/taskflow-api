# TaskFlow API

A secure RESTful API for task management, built with Flask and JWT authentication. Each user can sign up, log in, and manage their own tasks — full CRUD operations with user-specific data access.

## Features
- User authentication (Signup/Login) with JWT tokens
- Secure, user-specific task management (each user only sees their own tasks)
- Full CRUD operations (Create, Read, Update, Delete)
- Password hashing for security (Werkzeug)

## Tech Stack
- Python, Flask
- Flask-SQLAlchemy (SQLite database)
- Flask-JWT-Extended (authentication)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | /signup | Register a new user |
| POST | /login | Login and get JWT token |
| POST | /tasks | Create a new task (auth required) |
| GET | /tasks | Get all tasks for logged-in user |
| GET | /tasks/<id> | Get a specific task |
| PUT | /tasks/<id> | Update a task |
| DELETE | /tasks/<id> | Delete a task |

## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate it and install dependencies: `pip install flask flask-sqlalchemy flask-jwt-extended werkzeug`
4. Run: `python app.py`