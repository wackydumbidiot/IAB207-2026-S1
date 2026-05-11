from flask import Flask, render_template, redirect, url_for, request
from forms import CreateOrUpdateEventForm

def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.config["SECRET_KEY"] = "mysecretkey"

    @app.route("/")
    # Should be set to false in a production environment

    def index():
        return render_template("index.html")
    
    @app.route("/create-festival", methods=["GET", "POST"])
    def create_festival():
        form = CreateOrUpdateEventForm()

        print("REQUEST METHOD:", request.method)
        print("FORM DATA:", request.form)
        if form.validate_on_submit():
            return redirect(url_for("index"))
    
        print("FORM ERRORS:", form.errors)

        return render_template("create-festival.html", form=form)

    return app
    # app.secret_key = 'somesecretkey'
    # set the app configuration data 
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    # initialise db with flask app

    # Bootstrap5(app)