from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username", validators=[InputRequired()],)
    password = PasswordField("Password", validators=[InputRequired()],)
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)],)
    first_name = StringField("First Name", validators=[InputRequired()],)
    last_name = StringField("Last Name", validators=[InputRequired()],)


class LoginForm(FlaskForm):
    """Form for login"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    

class FeedbackForm(FlaskForm): 
    """Add feedback form""" 

    title = StringField("Title", validators=[InputRequired(), Length(max=100)],)
    content = StringField("Content", validators=[InputRequired()],) 


class DeleteForm(FlaskForm):
    """Delete form""" 