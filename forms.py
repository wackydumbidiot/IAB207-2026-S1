from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo

#user login form
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

#user registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email()])
    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

#booking form
class BookingForm(FlaskForm):
    quantity = IntegerField("Number of Tickets", validators=[InputRequired()])
    submit = SubmitField("Confirm Booking")
