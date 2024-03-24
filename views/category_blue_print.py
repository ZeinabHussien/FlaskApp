from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify,request

from models import db
from models.task_category import TaskCategory
import traceback



category_blueprint = Blueprint('TaskCategory', __name__)
# db = SQLAlchemy()

@category_blueprint.route('/category', methods=['POST'])
def post_categories():
    data = request.json
    name = data.get('name')
     

    if name is None:
        return jsonify({'error': 'Name is required'}), 400
    

    new_category = TaskCategory(name=name)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Task Category created ', 'category_id': new_category.id,'Category Name': new_category.name}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        print(traceback.print_exc())
        error=f"Transaction failed: {str(e)}"
        return jsonify({'message': error}), 400

   


