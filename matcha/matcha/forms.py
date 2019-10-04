from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from matcha.models import User, choices_gender, choices_age, choices_day, choices_month, choices_year

from datetime import date

class RegistrationForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm_Password',
                            validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender',
                            choices=choices_gender)
    day = SelectField('Day',
                        choices=choices_day)
    month = SelectField('Month',
                        choices=choices_month)
    year = SelectField('Year',
                        choices=choices_year)
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    # TODO FIX AGE CHECK
    def validate_year(self, year):
        today = date.today()
        current_year = year=year.data
        if int(current_year) < today.year:
            dif = today.year - int(current_year)
        else:
            dif = int(current_year) - today.year
        if dif < 18:
            raise ValidationError('Underage account. You need to be 18 years and older to create an account.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    gender = SelectField('Gender',
                            choices=choices_gender)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')