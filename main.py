from views.tasks_blue_print import tasks_blueprint
from views.category_blue_print import category_blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
import os

DB_URL=os.getenv('DB_URL')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db.init_app(app)


app.register_blueprint(tasks_blueprint)
app.register_blueprint(category_blueprint)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')