from flask import Flask, render_template

def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app

    @app.route("/")
    # Should be set to false in a production environment

    def index():
        return render_template("index.html")
    
    # app.debug = True

    return app
    # app.secret_key = 'somesecretkey'
    # set the app configuration data 
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    # initialise db with flask app

    # Bootstrap5(app)