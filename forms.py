from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired

class Register(FlaskForm):
    """Register new users"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class Login(FlaskForm):
    """User Log In form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])    

class Feedback_Form(FlaskForm):
    """User Submits Feedback"""
    feedback = TextAreaField("Add Feedback", validators=[InputRequired()])