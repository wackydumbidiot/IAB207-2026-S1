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
        from .models import Event

        search = request.args.get("search", "")
        category = request.args.get("category", "")
        query = Event.query

        if search:
            query = query.filter(Event.event_name.ilike(f"%{search}%"))

        if category:
            query = query.filter(Event.category == category)

        events = query.all()

        return render_template("index.html", events=events)
    
    @app.route("/event-created")
    def event_created():
        return render_template("event-created.html")
    
    @app.route("/booking-confirmed")
    def booking_confirmed():
        return render_template("booking-confirmed.html")
    
    @app.route("/view-event-details/<int:event_id>")
    def view_event_details(event_id):
        from .models import Event

        event = Event.query.get_or_404(event_id)

        return render_template("view-event-details.html", event=event)
    
    @app.route("/create-festival", methods=["GET", "POST"])
    def create_festival():
        from .forms import CreateOrUpdateEventForm
        from .models import Event

        form = CreateOrUpdateEventForm()
        

        print("REQUEST METHOD:", request.method)
        print("FORM DATA:", request.form)

        if form.validate_on_submit():
            uploaded_image = form.event_image.data

            uploaded_image.save("FestivalHub/static/img/" + uploaded_image.filename)
            event = Event(
                event_name = form.event_name.data,
                event_description = form.event_description.data,
                venue = form.venue.data,
                date = form.date.data,
                start_time = form.start_time.data,
                end_time = form.end_time.data,
                category = form.category.data,
                event_status = form.event_status.data,
                acknowledgement_of_country = form.acknowledgement.data,
                image = uploaded_image.filename,
                ticket_type = form.ticket_type.data,
                tickets_available = form.tickets_available.data
            )

            db.session.add(event)
            db.session.commit()
            print("Successfully created Event")
            
            # Always end with Redirect when form is valid
            return redirect(url_for("event_created"))
    
        print("FORM ERRORS:", form.errors)

        return render_template("create-festival.html", form=form)


    # app.secret_key = 'somesecretkey'
    # set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Festivaldata.sqlite'
    # initialise db with flask app
    db.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

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