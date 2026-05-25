from flask import Flask, app, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from datetime import date, time


db = SQLAlchemy()

def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.config["SECRET_KEY"] = "mysecretkey"

    @app.route("/")
    # Should be set to false in a production environment

    def index():
        from .models import Event

        events = Event.query.all()

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
        from .forms import CommentForm

        event = Event.query.get_or_404(event_id)
        form = CommentForm()

        return render_template("view-event-details.html", event=event, form=form)


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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from. models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))
    


# function to create demo data for testing and development purposes
    def demo_data():
        from .models import Event, User, Comment
        from werkzeug.security import generate_password_hash
        from datetime import date, time, datetime

        # Demo users

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
                    street_address="3 Demo Lane"
                )
            ]

            db.session.add_all(users)
            db.session.commit()


        # Demo events

        if Event.query.count() == 0:
            events = [
                Event(
                    event_name="Coldplay Live in Brisbane",
                    event_description="A major live music event featuring Coldplay with a full stadium experience, lights, visuals, and popular songs.",
                    category="Pop",
                    date=date(2026, 6, 12),
                    start_time=time(18, 30),
                    end_time=time(22, 30),
                    venue="Suncorp Stadium",
                    event_status="Open",
                    acknowledgement_of_country="No Acknowledgement of Country",
                    ticket_type="General Admission",
                    tickets_available=150,
                    image="coldplay.jpg"
                ),
                Event(
                    event_name="Ed Sheeran Acoustic Night",
                    event_description="An acoustic live music event featuring Ed Sheeran songs, relaxed vibes, and a strong focus on vocals and guitar.",
                    category="Pop",
                    date=date(2026, 7, 20),
                    start_time=time(19, 0),
                    end_time=time(22, 0),
                    venue="Riverstage",
                    event_status="Open",
                    acknowledgement_of_country="generic",
                    ticket_type="General Admission",
                    tickets_available=120,
                    image="edsheeran.jpg"
                ),
                Event(
                    event_name="Splendour in the Grass",
                    event_description="A large outdoor music festival with multiple artists, food stalls, live performances, and festival activities.",
                    category="Rock",
                    date=date(2026, 8, 5),
                    start_time=time(12, 0),
                    end_time=time(23, 0),
                    venue="Byron Bay",
                    event_status="Open",
                    acknowledgement_of_country="enhanced",
                    ticket_type="VIP",
                    tickets_available=80,
                    image="splendour-in-the-grass.jpg"
                ),
                Event(
                    event_name="Country Fest Queensland",
                    event_description="A country music festival featuring local and national country artists with a friendly outdoor atmosphere.",
                    category="Country",
                    date=date(2026, 9, 18),
                    start_time=time(14, 0),
                    end_time=time(22, 0),
                    venue="Toowoomba",
                    event_status="Open",
                    acknowledgement_of_country="generic",
                    ticket_type="General Admission",
                    tickets_available=100,
                    image="country-fest-queensland-2026.jpg"
                )
            ]

            db.session.add_all(events)
            db.session.commit()


        # Demo comments

        if Comment.query.count() == 0:
            first_event = Event.query.first()
            alice = User.query.filter_by(email="alice@example.com").first()
            bob = User.query.filter_by(email="bob@example.com").first()
            sean = User.query.filter_by(email="sean@example.com").first()

            comments = [
                Comment(
                    comment_text="Love Ed Sheeran but also amazing lineup this year!. Really excited to attend with my friends.",
                    created_at=datetime(2026, 3, 5),
                    event_id=first_event.id,
                    user_id=alice.id
                ),
                Comment(
                    comment_text="The venue looks great, the ticket options and the pricing seems pretty reasonable. Other than that, I cannot wait for more future events!",
                    created_at=datetime(2026, 3, 7),
                    event_id=first_event.id,
                    user_id=bob.id
                ),
                Comment(
                    comment_text="Such a good venue would recommend, good service.",
                    created_at=datetime(2026, 3, 7),
                    event_id=first_event.id,
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

    from . import auth
    app.register_blueprint(auth.auth_bp)
    
    return app