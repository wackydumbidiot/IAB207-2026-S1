<<<<<<< HEAD
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm, CreateOrUpdateEventForm
from .. import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/<id>')
def show(id):
    destination = get_destination()
    # create the comment form
    cform = CommentForm()    
    return render_template('destinations/show.html', destination=destination, form=cform)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')



# Comment for event page 
@auth_bp.route('/<id>/comment', methods=['GET', 'POST'])  
def comment(id):  
    form = CommentForm()  
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query
      comment = Comment(text=form.text.data, event=event) 
      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      # flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))
=======
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm, CreateOrUpdateEventForm
from . import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
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


@auth_bp.route('/register', methods=['GET', 'POST'])
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


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))
>>>>>>> a3a6a91 (Add event comments and demo data)
