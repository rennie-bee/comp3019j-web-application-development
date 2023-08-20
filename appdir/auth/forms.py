from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from wtforms.widgets import TextInput, PasswordInput
from wtforms.fields import simple
from ..models import User


# form used to let user login
class LoginForm(FlaskForm):
    # user inputs email address, whose length is between 1 and 64, required in email format
    username = StringField('Username', validators=[DataRequired(message='Username can not be empty'), Length(1, 64)])
    # user inputs account password, whose length is between 1 and 64, assigned with a class called form-control
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 64)],
                             render_kw={'class': 'form-control'})
    # user submits the form
    submit = SubmitField('Sign In')


# form used to let user register
class RegistrationForm(FlaskForm):
    # Regexp: for the username, the last two parameters work when faults happened. Letters, numbers, dots,
    # and underscores are allowed in the username.
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0,
                                                                                         'Letters, numbers, dots, and '
                                                                                         'underscores are allowed in '
                                                                                         'username.')])
    # user inputs account password, whose length is between 1 and 64
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 64)])
    # user inputs password again. 2 passwords need to be identical.
    password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(1, 64)])
    # user submits the register form
    submit = SubmitField('Register')
