from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this' 
jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return {"message": "TaskFlow API is running!"}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Check karo user pehle se exist toh nahi karta
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=False,
        user_id=current_user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user_id).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})
if __name__ == '__main__':
    app.run(debug=True)
