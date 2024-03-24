from models import db
class TaskCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80) , unique=True)
    def __repr__(self):
        return '<Category %r>' % self.name
    


    