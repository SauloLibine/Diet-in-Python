from database import db
from datetime import datetime

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    good_for_diet = db.Column(db.Boolean, default=True)

  
