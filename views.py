from flask import Blueprint

from flask_login import login_required, current_user

from .models import Order

from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return '<h1>Starter code for assignment 3<h1>'

@main_bp.route('/bookings')

@login_required
def bookings():

    orders = db.session.scalars(
        db.select(Order).where(
            Order.user_id == current_user.id
        )
    ).all()

    return render_template(
        'view-bookings.html',
        orders=orders)
