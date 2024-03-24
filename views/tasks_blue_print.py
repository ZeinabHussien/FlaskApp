from flask import Blueprint, jsonify,request
from views.category_blue_print import TaskCategory
from models import db
from models.task_category import TaskCategory
from models.tasks import Task
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime

tasks_blueprint = Blueprint('tasks', __name__)
# db = SQLAlchemy()

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    result= db.session.query(Task, TaskCategory.name).join(TaskCategory, Task.category_id == TaskCategory.id).filter(Task.id == task_id,Task.status=='A').first()
    
    if result is not None:
        task, category_name = result
        task_data = {'id': task.id, 'status':task.status,'priority': task.priority,'title': task.title, 'description': task.description, 'completed': task.completed, 'category':category_name}
        return jsonify(task_data), 200
    else:
        return jsonify({'error': 'Task not found'}), 404



@tasks_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    category_name = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    priority= request.args.get('priority')

    task_data = []

        
    query =  db.session.query(Task, TaskCategory.name).join(TaskCategory, Task.category_id == TaskCategory.id).filter(Task.status == 'A')
    if category_name:
        query =query.filter(func.lower(TaskCategory.name).ilike(f'%{category_name.lower()}%'))
    if start_date:
        if is_valid_date(start_date):
            query =query.filter(Task.due_date > start_date)
        else:
            return jsonify({'error': 'Invalid Date'}), 400


    if end_date:
        if is_valid_date(end_date):
            query =query.filter(Task.due_date < end_date)
        else:
            return jsonify({'error': 'Invalid Date'}), 400
    if priority:
        prioriry= priority.lower()
        query =query.filter(Task.priority == priority)



    tasks= query.all()
    for task ,category_name in tasks:
            task_info = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'category': category_name  ,
                'due_date':task.due_date,
                'status':task.status,
                'priority':task.priority
            }
            task_data.append(task_info)


    return jsonify(task_data)

@tasks_blueprint.route('/tasks', methods=['POST'])
def post_tasks():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False) 
    category_id= data.get('category_id')
    status= data.get('status')
    due_date = data.get('due_date')
    priority= data.get('priority')
    
    if title  is None or title =='' or category_id is None :
        return jsonify({'error': 'Required fields: Title and Category '}), 400
    if priority:
        valid_priorities = {'high', 'normal', 'low'}  # Set of valid priorities
        priority_lower = priority.lower()  # Convert priority to lowercase
        if priority_lower not in valid_priorities:
             return jsonify({'error': 'Valid Priorities are: high, normal,low '}), 400

        

 
    category = TaskCategory.query.get(category_id)
    if category:

        new_task = Task( title=title,due_date=due_date, priority=priority,description=description,status=status,completed=completed,category_id= category_id)
        print(new_task.status)
        try:
            db.session.add(new_task)
            db.session.commit()

            return jsonify({'message': 'Task created ', 'task':{'priority':new_task.priority,'status':new_task.status,'due_date':new_task.due_date,'task_id': new_task.id,'title': new_task.title,'description':new_task.description,'completed':new_task.completed,'category_id':new_task.category_id}}), 201

        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            error=f"Transaction failed: {str(e)}"
            return jsonify({'message': error}), 400
    
    else:
        return jsonify({'error': 'Categroy Not found'}), 400

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_tasks(task_id):
    task = Task.query.get(task_id)

    if task:
        # db.session.delete(task)
        task.status='D'
        db.session.commit()
        return jsonify({'message': 'Task deleted '}), 200
    else:
        return jsonify({'error': 'No Task Found'}), 404
    

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    if task:
        data = request.json
        print(data)
        if 'title' in data:
            task.title= data.get('title')
           

        if 'description' in data:
            task.description = data.get('description')
        if 'completed' in data:
            task.completed = data.get('completed')
        if 'category_id' in data:
            new_category= TaskCategory.query.get(data.get('category_id'))
            if new_category is None:
                return jsonify({'error': 'Categroy Not found'}), 400
            else:
                task.category_id= data.get('category_id')
        if 'priority' in data:
            task.priority= data.get('priority')

        if 'due_date' in data:
            if is_valid_date(data.get('due_date')):
                 task.priority= data.get('due_date')
            else:
                return jsonify({'error': 'Invalid Date'}), 400
               

        try:
            db.session.commit()
            return jsonify({'message': 'Task updated successfully','task':{'priority':task.priority,'status':task.status,'due_date':task.due_date,'task_id': task.id,'title': task.title,'description':task.description,'completed':task.completed,'category_id':task.category_id}}), 200
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            error=f"Transaction failed: {str(e)}"
            return jsonify({'message': error}), 400


    else:
        return jsonify({'error': 'No Task Found'}), 404
    

def is_valid_date(start_date_str):
    try:
        # Attempt to parse the start date string into a datetime object
        datetime.strptime(start_date_str, '%m-%d-%Y')
        # If parsing succeeds, the date is valid
        return True
    except ValueError:
        # If parsing fails, the date is invalid
        return False

