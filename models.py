from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Order', backref='user', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    date = db.Column(db.DateTime, nullable=False)

    location = db.Column(db.String(100), nullable=False)

    capacity = db.Column(db.Integer, nullable=False)

    orders = db.relationship('Order', backref='event', lazy=True)


class booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(db.String(20), unique=True, nullable=False)

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)


