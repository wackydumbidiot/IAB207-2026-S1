from . import db
from datetime import datetime
from flask_login import UserMixin

# class User(db.Model, UserMixin):
#     pass

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(20), nullable=False)
    ticket_type = db.Column(db.String(20), nullable=False)
    tickets_available = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    # String print method
    def __repr__(self):
        return f"Name: {self.name}"

# class Comment(db.Model):
#     pass

# class Order(db.Model):
#     pass