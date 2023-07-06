from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()

class CharacterForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    house = StringField('House', validators = [DataRequired()])
    nationality = StringField('Nationality')
    occupation = StringField('Occupation')
    books_appeared_in = IntegerField('Books Appeared In (#)', validators = [DataRequired()])
    submit_button = SubmitField()