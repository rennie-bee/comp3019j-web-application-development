from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from ..models import User


