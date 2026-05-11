from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

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
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')



# import flask - from 'package' import 'Class'
from flask import Flask 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = 'somesecretkey'
    # set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    # initialise db with flask app
    db.init_app(app)

    Bootstrap5(app)
    
    # initialise the login manager
    login_manager = LoginManager()
    
    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return db.session.scalar(db.select(User).where(User.id==user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)
    
    return app
