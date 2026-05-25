from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    # One user can post many comments
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f"User: {self.email}"

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
    event_status = db.Column(db.String(20), nullable=False)
    acknowledgement_of_country = db.Column(db.String(100), nullable=False)
    ticket_type = db.Column(db.String(20), nullable=False)
    tickets_available = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='event', lazy=True)

    # String print method
    def __repr__(self):
        return f"Name: {self.event_name}"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Comment: {self.comment_text}"
# class Order(db.Model):
#     pass