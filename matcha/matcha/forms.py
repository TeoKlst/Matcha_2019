from matcha import sql
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from matcha.models import choices_gender, choices_day, choices_month, choices_year, choices_sexpreference, \
                            choices_gap, choices_tags, choices_geo, choices_gap_fame, choices_gap_age, \
                            choices_asc_desc, choices_sort
from datetime import date

# Python Classes converted to html forms within templates

class RegistrationForm(FlaskForm):
    firstname           = StringField('First name',
                                    validators=[DataRequired(), Length(min=2, max=20)])
    lastname            = StringField('Last name',
                                    validators=[DataRequired(), Length(min=2, max=20)])
    username            = StringField('Username',
                                    validators=[DataRequired(), Length(min=2, max=20)])
    email               = StringField('Email',
                                    validators=[DataRequired(), Email()])
    password_field      = PasswordField('Password',
                                    validators=[DataRequired(), Length(min=10)])
    confirm_password    = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password_field')])
    gender              = SelectField('Gender',
                                    choices=choices_gender)
    day                 = SelectField('Day',
                                    choices=choices_day)
    month               = SelectField('Month',
                                    choices=choices_month)
    year                = SelectField('Year',
                                    choices=choices_year)
    submit              = SubmitField('Sign Up')

    def validate_username(self, username):
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=:username", {'username': username.data})
        user_data = cur.fetchone()
        conn.close()
        if user_data:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=:email", {'email': email.data})
        user_data = cur.fetchone()
        conn.close()
        if user_data:
            raise ValidationError('That email is taken. Please choose a different one.')

    # TODO Validate age check
    def validate_year(self, year):
        today = date.today()
        current_year = year=year.data
        if int(current_year) < today.year:
            dif = today.year - int(current_year)
        else:
            dif = int(current_year) - today.year
        if dif < 18:
            raise ValidationError('Underage account. You need to be 18 years and older to create an account.')

    # TODO validate_passwordComplexity(self, password_field):

class LoginForm(FlaskForm):
    email       = StringField('Email',
                            validators=[DataRequired(), Email()])
    password    = PasswordField('Password',
                            validators=[DataRequired()])
    remember    = BooleanField('Remember Me')
    submit      = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    firstname   = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname    = StringField('Last name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    username    = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email       = StringField('Email',
                            validators=[DataRequired(), Email()])
    gender      = SelectField('Gender',
                            choices=choices_gender)
    sexual_pref = SelectField('Sex Pref',
                            choices=choices_sexpreference)
    biography   = TextAreaField('Biography')
    user_tag1   =SelectField('User Tag1',
                            choices=choices_tags)
    user_tag2   =SelectField('User Tag1',
                            choices=choices_tags)
    user_tag3   =SelectField('User Tag1',
                            choices=choices_tags)                          
    user_tag4   =SelectField('User Tag1',
                            choices=choices_tags)   
    user_tag5   =SelectField('User Tag1',
                            choices=choices_tags)
    geo_tag     =SelectField('Geo Tag',
                            choices=choices_geo)
    picture_p   = FileField('Update Profile Picture', 
                            validators=[FileAllowed(['jpg', 'png'])])
    picture_1   = FileField('Update Picture 1', 
                            validators=[FileAllowed(['jpg', 'png'])])
    picture_2   = FileField('Update Picture 2', 
                            validators=[FileAllowed(['jpg', 'png'])])
    picture_3   = FileField('Update Picture 3', 
                            validators=[FileAllowed(['jpg', 'png'])])
    picture_4   = FileField('Update Picture 4', 
                            validators=[FileAllowed(['jpg', 'png'])])
    picture_5   = FileField('Update Picture 5', 
                            validators=[FileAllowed(['jpg', 'png'])])
    submit      = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            conn = sql.connect('matcha\\users.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=:username", {'username': username.data})
            user_data = cur.fetchone()
            conn.close()
            if user_data:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            conn = sql.connect('matcha\\users.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email=:email", {'email': email.data})
            user_data = cur.fetchone()
            conn.close()
            if user_data:
                raise ValidationError('That email is taken. Please choose a different one.')


class MessagesForm(FlaskForm):
    message_content = TextAreaField('Message Content',
                                    validators=[DataRequired()])
    submit          = SubmitField('Send')


class SearchForm(FlaskForm):
    age_min         = SelectField('Min. Age',
                                choices=choices_gap_age)
    age_max         = SelectField('Max Age',
                                choices=choices_gap_age)
    fame_rating_min = SelectField('Min. Fame',
                                choices=choices_gap_fame)
    fame_rating_max = SelectField('Max Fame',
                                choices=choices_gap_fame)
    location        = SelectField('Location',
                                choices=[])
    tag1            =SelectField('Tag1',
                                choices=choices_tags)
    tag2            =SelectField('Tag2',
                                choices=choices_tags)
    tag3            =SelectField('Tag3',
                                choices=choices_tags)
    tag4            =SelectField('Tag4',
                                choices=choices_tags)
    tag5            =SelectField('Tag5',
                            choices=choices_tags)
    submit          = SubmitField('Search')

class SortForm(FlaskForm):
    field_select    = SelectField('Sort Critera',
                                choices=choices_sort)
    type_sort       = SelectField('Asc or Desc',
                                choices=choices_asc_desc)
    submit          = SubmitField('Sort')

class RequestResetForm(FlaskForm):
    email       = StringField('Email',
                            validators=[DataRequired(), Email()])
    submit          = SubmitField('Request Password Reset')

    def validate_email(self, email):
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=:email", {'email': email.data})
        user_data = cur.fetchone()
        conn.close()
        if user_data is None:
            raise ValidationError('No account with that email. Please check email again or register.')

class ResetPasswordForm(FlaskForm):
    password_field      = PasswordField('Password',
                                    validators=[DataRequired(), Length(min=8)])
    confirm_password    = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password_field')])
    submit          = SubmitField('Request Password Reset')