from sqlalchemy import DateTime
from models import db
from datetime import datetime, timedelta
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80) )
    description = db.Column(db.String(80) )
    status = db.Column(db.String(80) )
    priority = db.Column(db.String(80) ,default= 'normal')
    completed = db.Column(db.Boolean())
    category_id = db.Column(db.Integer, db.ForeignKey('task_category.id'))
    due_date = db.Column(DateTime,default=lambda: datetime.now() + timedelta(days=2))
    def __repr__(self):
        return '<Task %r>' % self.title