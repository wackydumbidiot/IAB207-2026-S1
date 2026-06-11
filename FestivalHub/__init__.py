from flask import Flask, render_template, redirect, url_for, request, flash 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user

db = SQLAlchemy()

def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.config["SECRET_KEY"] = "mysecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Festivaldata.sqlite"

 # initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    @app.route("/")
    # Should be set to false in a production environment

    def index():
        from .models import Event

        #raise Exception("Execption 500 page")

        search = request.args.get("search", "")
        category = request.args.get("category", "")
        status = request.args.get("event_status", "")
        query = Event.query

        if search:
            query = query.filter(Event.event_name.ilike(f"%{search}%"))

        if category:
            query = query.filter(Event.category == category)

        if status:
            query = query.filter(Event.event_status == status)

        events = query.all()

        noResultsMessage = None

        if not events:
            if search and category and status:
                noResultsMessage = f"No results found for event '{search}' with category '{category}' and with status '{status}'."
            elif search and category:
                noResultsMessage = f"No results found for event '{search}' with category '{category}'."
            elif category and status:
                noResultsMessage = f"No results found for category '{category}' with status '{status}'."
            elif search:
                noResultsMessage = f"No results found for event '{search}'."
            elif category:
                noResultsMessage = f"No results found for category '{category}'."
            elif status:
                noResultsMessage = f"No results found for status '{status}'."

        return render_template("index.html", events=events, noResultsMessage=noResultsMessage)
    
    @app.route("/event-created")
    def event_created():
        return render_template("event-created.html")
    
    @app.route("/booking-confirmed")
    def booking_confirmed():
        return render_template("booking-confirmed.html")
    
    @app.route("/view-event-details/<int:event_id>")
    def view_event_details(event_id):
        from .models import Event
        from .forms import CommentForm

        event = Event.query.get_or_404(event_id)
        form = CommentForm()

        return render_template(
            "view-event-details.html",
            event=event,
            form=form
        )
    

    @app.route("/view-event-details/<int:event_id>/comment", methods=["POST"])
    @login_required
    def post_comment(event_id):
        from .models import Event, Comment
        from .forms import CommentForm

        event = Event.query.get_or_404(event_id)
        form = CommentForm()

        if form.validate_on_submit():
            comment = Comment(
                comment_text=form.text.data,
                event_id=event.id,
                user_id=current_user.id
            )

            db.session.add(comment)
            db.session.commit()

            flash("Your comment has been posted.", "success")

        return redirect(url_for("view_event_details", event_id=event.id))

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
                event_status = "Open",
                acknowledgement_of_country = form.acknowledgement.data,
                image = uploaded_image.filename,
                ticket_type = form.ticket_type.data,
                tickets_price = float(form.tickets_price.data),
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

    def demo_data():
        from .models import Event, User, Comment
        from werkzeug.security import generate_password_hash
        from datetime import datetime, date, time

        if Event.query.count() == 0:
            event = Event(
                event_name="Ed Sheeran",
                event_description="A live music event featuring Ed Sheeran with a relaxed acoustic atmosphere.",
                category="Pop",
                date=date(2026, 7, 20),
                start_time=time(19, 0),
                end_time=time(22, 0),
                venue="Riverstage",
                event_status="Open",
                acknowledgement_of_country="No Acknowledgement of Country",
                ticket_type="General Admission",
                tickets_price="10.0",
                tickets_available=120,
                image="edsheeran.jpg"
            )

            db.session.add(event)
            db.session.commit()

        if User.query.count() == 0:
            users = [
                User(
                    first_name="Alice",
                    surname="Smith",
                    email="alice@example.com",
                    password_hash=generate_password_hash("password123"),
                    contact_number="0400000001",
                    street_address="1 Demo Street"
                ),
                User(
                    first_name="Bob",
                    surname="Johnson",
                    email="bob@example.com",
                    password_hash=generate_password_hash("password123"),
                    contact_number="0400000002",
                    street_address="2 Demo Street"
                ),
                User(
                    first_name="Sean",
                    surname="Dewantoro",
                    email="sean@example.com",
                    password_hash=generate_password_hash("password123"),
                    contact_number="0400000003",
                    street_address="3 Demo Street"
                )
            ]

            db.session.add_all(users)
            db.session.commit()

        if Comment.query.count() == 0:
            event = Event.query.first()
            alice = User.query.filter_by(email="alice@example.com").first()
            bob = User.query.filter_by(email="bob@example.com").first()
            sean = User.query.filter_by(email="sean@example.com").first()

            comments = [
                Comment(
                    comment_text="Love Ed Sheeran but also amazing lineup this year! Really excited to attend with my friends.",
                    created_at=datetime(2026, 3, 5),
                    event_id=event.id,
                    user_id=alice.id
                ),
                Comment(
                    comment_text="The venue looks great, and the ticket options and pricing seem pretty reasonable.",
                    created_at=datetime(2026, 3, 7),
                    event_id=event.id,
                    user_id=bob.id
                ),
                Comment(
                    comment_text="Such a good venue, would recommend. Good service.",
                    created_at=datetime(2026, 3, 7),
                    event_id=event.id,
                    user_id=sean.id
                )
            ]

            db.session.add_all(comments)
            db.session.commit()

    with app.app_context():
        db.create_all()
        demo_data()

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
    # initialise the login manager




    from . import auth
    app.register_blueprint(auth.auth_bp)

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template("404_not_found.html"), 404
        
    @app.errorhandler(500)
    def internalError(error):
        return render_template("500_internal_error.html"), 500
    
    return app