<<<<<<< HEAD
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.email == form.user_name.data)
        )

        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash("Incorrect email or password.")
            return redirect(url_for("auth.login"))

        login_user(user)

        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)

        return redirect(url_for("index"))

    return render_template("user.html", form=form, heading="Login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = db.session.scalar(
            db.select(User).where(User.email == form.email.data)
        )

        if existing_user:
            flash("This email is already registered.")
            return redirect(url_for("auth.register"))

        user = User(
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            contact_number=form.contact_number.data,
            street_address=form.street_address.data
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("user.html", form=form, heading="Register")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))
=======
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from .models import User
from .forms import LoginForm, RegisterForm
from .import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None

    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data

        user = db.session.scalar(
            db.select(User).where(User.name == user_name)
        )

        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'

        if error is None:
            login_user(user)

            nextp = request.args.get('next')

            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('index'))

            return redirect(nextp)

        flash(error)

    return render_template('user.html', form=login_form, heading='Login')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        existing_user = db.session.scalar(
            db.select(User).where(User.name == register_form.user_name.data)
        )

        existing_email = db.session.scalar(
            db.select(User).where(User.email == register_form.email.data)
        )

        if existing_user:
            flash('Username already exists')
        elif existing_email:
            flash('Email already exists')
        else:
            hashed_password = generate_password_hash(
                register_form.password.data
            )

            user = User(
                name=register_form.user_name.data,
                email=register_form.email.data,
                password_hash=hashed_password
            )

            db.session.add(user)
            db.session.commit()

            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))

    return render_template('user.html', form=register_form, heading='Register')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))
>>>>>>> 440d1fe (added database and user features)
