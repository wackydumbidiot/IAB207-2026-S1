from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Festivaldata.sqlite"

    db.init_app(app)
    Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/event-created")
    def event_created():
        return render_template("event-created.html")

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

        if form.validate_on_submit():
            uploaded_image = form.event_image.data
            uploaded_image.save(
                "FestivalHub/static/img/" + uploaded_image.filename
            )

            event = Event(
                event_name=form.event_name.data,
                event_description=form.event_description.data,
                venue=form.venue.data,
                date=form.date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                category=form.category.data,
                image=uploaded_image.filename,
                ticket_type=form.ticket_type.data,
                tickets_available=form.tickets_available.data
            )

            db.session.add(event)
            db.session.commit()

            return redirect(url_for("event_created"))

        return render_template("create-festival.html", form=form)
    
    @app.route('/bookings')
    @login_required
    def bookings():

        from .models import Order

        orders = Order.query.filter_by(
        user_id=current_user.id
        ).all()

        return render_template(
        'view-bookings.html',
        orders=orders
        )



    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(
            db.select(User).where(User.id == user_id)
        )

    with app.app_context():
        from .models import User, Event, Order
        db.create_all()

    from . import auth
    app.register_blueprint(auth.auth_bp)

    return app