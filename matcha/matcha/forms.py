from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from matcha.models import User, choices_gender, choices_age

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
    age = StringField('Age',
                           validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Gender',
                            choices=choices_gender)
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    # def validate_age(self, age):
    #     if age < 18:
    #         raise ValidationError('Invalid age')


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
    age = StringField('Age',
                           validators=[DataRequired(), Length(min=2, max=20)])
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