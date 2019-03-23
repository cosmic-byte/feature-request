from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = TextField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
