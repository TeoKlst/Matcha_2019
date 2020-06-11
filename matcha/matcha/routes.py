import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from matcha import app, db, bcrypt
from matcha.forms import RegistrationForm, LoginForm, UpdateAccountForm
from matcha.models import User, Like, Message, Images, Tags, Post        
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date

# Templating engine that flask uses is Jinja2

posts = [
    {
        'author': 'Dude1',
        'title': 'Some1 Title',
        'content':  'Contents1',
        'date_posted': 'June 06 2020'
    },
    {
        'author': 'Dude2',
        'title': 'Some2 Title',
        'content':  'Contents2',
        'date_posted': 'June 06 2020'
    },
    {
        'author': 'Dude3',
        'title': 'TestTitle3',
        'content': 'Contents3',
        'date_posted': 'June 06 2020'
    },
    {
        'author': 'Dude4',
        'title': 'TestTitle4',
        'content': 'Contents4',
        'date_posted': 'June 06 2020'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/frontpage')
def frontpage():
    return render_template('frontpage.html', title='FrontPage')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        today = date.today()
        born = date(int(form.year.data), int(form.month.data), int(form.day.data))
        hashed_password = bcrypt.generate_password_hash(form.password_field.data).decode('utf-8')
        user = User(firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    age=today.year - born.year - ((today.month, today.day) < (born.month, born.day)),
                    birthdate=born,
                    gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account {form.username.data} has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstname  = form.firstname.data
        current_user.lastname   = form.lastname.data
        current_user.username   = form.username.data
        current_user.email      = form.email.data
        current_user.gender     = form.gender.data 
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data  = current_user.lastname
        form.username.data  = current_user.username
        form.email.data     = current_user.email
        form.gender.data    = current_user.gender
    # Passing image file to account here
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
