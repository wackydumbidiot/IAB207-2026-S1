from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
# from flask_bcrypt import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, logout_user
# from ..models import User
# from .forms import LoginForm, RegisterForm
# from .. import db
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, SelectField, IntegerField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name'),Email("Please enter a valid email")])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired("Enter your first name")
    ])
    surname = StringField("Surname", validators=[InputRequired("Enter your surname")
    ])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    contact_number = StringField("Contact Number", validators=[InputRequired("Enter your contact number")])
    street_address = StringField("Street Address", validators=[InputRequired("Enter your street address")])

    # submit button
    submit = SubmitField("Register")



# creates the CreateOrUpdateEventForm information
class CreateOrUpdateEventForm(FlaskForm):
    event_name=StringField("Event Name", validators=[InputRequired('Event name cannot be empty.')])
    event_description = TextAreaField("Description", validators=[InputRequired('Description cannot be empty.')])
    venue = StringField("Venue", validators=[InputRequired('Venue cannot be empty.')])
    tickets_available = StringField("Venue", validators=[InputRequired('Venue cannot be empty.')])
    date = DateField("Date", validators=[InputRequired('Please select a date.')])
    start_time = TimeField("Start Time", validators=[InputRequired('Please select a start time.')])
    end_time = TimeField("End Time", validators=[InputRequired('Please select an end time.')])

    category = SelectField("Category", choices=[
                                                ("", "Select Category"),
                                                ("Rock", "Rock"),
                                                ("EDM", "EDM"),
                                                ("Jazz", "Jazz"),
                                                ("Pop", "Pop"),
                                                ("Country", "Country")
                                                ],
                                                validators=[InputRequired("Please select a category")])
    
    event_status = SelectField("Status", choices=[
                                                ("", "Select Status"),
                                                ("Open", "Open"),
                                                ("Inactive", "Inactive"),
                                                ("Sold Out", "Sold Out"),
                                                ("Cancelled", "Cancelled")
                                                ],
                                                validators=[InputRequired("Please select a status")])
    
    acknowledgement = SelectField("Acknowledgement of Country:", choices=[
        ("", "Select Acknowledge of Country"),
        ("No Acknowledgement of Country", "No Acknowledgement of Country"),
        ("generic", "Acknowledgement of Country: generic"),
        ("enhanced", "Acknowledgement of Country: enhanced")
    ],
    validators=[InputRequired(message="Please select an acknowledgement option.")])

    ticket_type = SelectField("Ticket Type:", choices=[("", "Select Ticket Type"),
                                                       ("General Admission", "General Admission"),
                                                       ("VIP", "VIP")],
    validators=[InputRequired(message="Please select a ticket type.")])

    tickets_available = IntegerField("Tickets Available:", validators=[InputRequired(message="Please enter number of tickets."), 
                                                                    NumberRange(min=1, message="Tickets must be at least 1.")])

    event_image = FileField("Event Image:", validators=[InputRequired(message="Please upload an event image.")])

    submit = SubmitField("Create Event", validators=[InputRequired()])

    # creates the comment form information
class CommentForm(FlaskForm):
    text = TextAreaField("Your Comment:", validators=[
        InputRequired("Comment cannot be empty."),
        Length(max=500, message="Comment cannot exceed more than 500 characters.")
    ])

    # submit button
    submit = SubmitField("Post Comment")