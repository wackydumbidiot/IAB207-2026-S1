from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Order
from . import db


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/bookings')
@login_required
def bookings():
    orders = db.session.scalars(
        db.select(Order).where(Order.user_id == current_user.id)
    ).all()

    return render_template('view-bookings.html', orders=orders)
