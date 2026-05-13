from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.config["SECRET_KEY"] = "mysecretkey"

    @app.route("/")
    # Should be set to false in a production environment

    def index():
        return render_template("index.html")
    
    @app.route("/create-festival", methods=["GET", "POST"])
    def create_festival():
        from .forms import CreateOrUpdateEventForm
        form = CreateOrUpdateEventForm()

        print("REQUEST METHOD:", request.method)
        print("FORM DATA:", request.form)

        if form.validate_on_submit():
            #event = {}
            return render_template("event-created.html")
    
        print("FORM ERRORS:", form.errors)

        return render_template("create-festival.html", form=form)


    # app.secret_key = 'somesecretkey'
    # set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    # initialise db with flask app
    db.init_app(app)

    Bootstrap5(app)

    # initialise the login manager
    # login_manager = LoginManager()
    
    # # set the name of the login function that lets user login
    # # in our case it is auth.login (blueprintname.viewfunction name)
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # # create a user loader function takes userid and returns User
    # # Importing inside the create_app function avoids circular references

    # from .models import User, Event
    # @login_manager.user_loader
    # def load_user(user_id):
    #    return db.session.scalar(db.select(User).where(User.id==user_id))

    # from . import views
    # app.register_blueprint(views.main_bp)

    # from . import auth
    # app.register_blueprint(auth.auth_bp)
    
    return app