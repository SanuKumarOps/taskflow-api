from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# App initialize karna
app = Flask(__name__)

# Database config — SQLite file 'tasks.db' naam se banegi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Task model/table define karna
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    # Ye function task ko JSON format mein convert karega response ke liye
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

# Database tables create karna (agar pehle se nahi bani hain)
with app.app_context():
    db.create_all()

# Test route — check karne ke liye ki server chal raha hai
@app.route('/')
def home():
    return {"message": "TaskFlow API is running!"}
# 1. CREATE - Naya task add karna
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=False
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# 2. READ - Saare tasks dekhna
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# 3. READ - Ek specific task dekhna (ID se)
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

# 4. UPDATE - Task update karna
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.to_dict())

# 5. DELETE - Task delete karna
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})
if __name__ == '__main__':
    app.run(debug=True)
