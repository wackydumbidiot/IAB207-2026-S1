from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from .models import User
from .forms import LoginForm, RegisterForm
from . import db


auth_bp = Blueprint('auth', __name__)

#create login form
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #Validate login
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.name == form.user_name.data)
        )

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))

        flash('Incorrect username or password')

    return render_template('user.html', form=form, heading='Login')

# create registration form
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    #validate registration form
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)

        user = User(
            name=form.user_name.data,
            email=form.email.data,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('user.html', form=form, heading='Register')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

