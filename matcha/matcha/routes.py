import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from matcha import app, bcrypt, sql
from matcha.forms import RegistrationForm, LoginForm, UpdateAccountForm, MessagesForm
# from matcha.models import Like, Message, Images, Tags, Post    
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, timedelta, datetime

# Templating engine that flask uses is Jinja2
db = 1
from matcha.classes import User, Message
from matcha.dbfunctions import register_userTest, update_user, update_image, create_message

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
    # print (current_user)
    print (current_user.is_authenticated)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/frontpage')
def frontpage():
    return render_template('frontpage.html', title='FrontPage')

# TODO Close db conn
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        today = date.today()
        birthdate = date(int(form.year.data), int(form.month.data), int(form.day.data))
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        hashed_password = bcrypt.generate_password_hash(form.password_field.data).decode('utf-8')

        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        user = User('user_id', form.firstname.data, form.lastname.data, age, birthdate,
                form.username.data, form.email.data, hashed_password, form.gender.data, 'sexual_pref',
                'biography', 'famerating', 'image_file_p', 'image_file_1', 'image_file_2',
                'image_file_3', 'image_file_4', 'image_file_5')
        register_userTest(conn, cur, user)
        # register_user(conn, cur, user)
        conn.close()
        flash(f'Your account {form.username.data} has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# Close db conn
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=:email", {'email': form.email.data})
        user_data = cur.fetchone()

        i = 0
        for data in user_data:
            print(str(i), data)
            i = i + 1
        # print(user_data)

        user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4],
                    user_data[5], user_data[6], user_data[7], user_data[8], user_data[9],
                    user_data[10], user_data[11], user_data[12], user_data[13], user_data[14],
                    user_data[15], user_data[16], user_data[17])

        conn.close()
        if user_data and bcrypt.check_password_hash(user.password, form.password.data):
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

# TODO Make 2nd high res image for viewwing
# Delete older image of user when a new one is uploaded
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

# TODO Update user information with a cleaner/lighter method
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()

        # ------ Image Data ------
        img_type = None
        picture_file = None
        if form.picture_p.data:
            img_type = 'image_file_p'
            picture_file = save_picture(form.picture_p.data)
        elif form.picture_1.data:
            img_type = 'image_file_1'
            picture_file = save_picture(form.picture_1.data)
        elif form.picture_2.data:
            img_type = 'image_file_2'
            picture_file = save_picture(form.picture_2.data)
        elif form.picture_3.data:
            img_type = 'image_file_3'
            picture_file = save_picture(form.picture_3.data)
        elif form.picture_4.data:
            img_type = 'image_file_4'
            picture_file = save_picture(form.picture_4.data)
        elif form.picture_5.data:
            img_type = 'image_file_5'
            picture_file = save_picture(form.picture_5.data)
        if img_type != None:
            img = picture_file
            update_image(conn, cur, current_user, img_type, img)

        user = User('user_id', form.firstname.data, form.lastname.data, 'age', 'birthdate',
                form.username.data, form.email.data, 'hashed_password', form.gender.data, 'sexual_pref',
                form.biography.data, 'famerating', 'image_file_p', 'image_file_1', 'image_file_2',
                'image_file_3', 'image_file_4', 'image_file_5')
        update_user(conn, cur, user)
        conn.close()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data  = current_user.lastname
        form.username.data  = current_user.username
        form.email.data     = current_user.email
        form.gender.data    = current_user.gender
        form.biography.data = current_user.biography
    # Passing image file to account here (Maybe push to GET?)
    image_file_p = url_for('static', filename='profile_pics/' + current_user.image_file_p)
    image_file_1 = url_for('static', filename='profile_pics/' + current_user.image_file_1) if current_user.image_file_1 else None
    image_file_2 = url_for('static', filename='profile_pics/' + current_user.image_file_2) if current_user.image_file_2 else None
    image_file_3 = url_for('static', filename='profile_pics/' + current_user.image_file_3) if current_user.image_file_3 else None
    image_file_4 = url_for('static', filename='profile_pics/' + current_user.image_file_4) if current_user.image_file_4 else None
    image_file_5 = url_for('static', filename='profile_pics/' + current_user.image_file_5) if current_user.image_file_5 else None
    images = [image_file_1, image_file_2, image_file_3, image_file_4, image_file_5]
    return render_template('account.html', title='Account', image_file_p=image_file_p, images=images, form=form)

@app.route('/inbox')
@login_required
def inbox():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    # cur.execute("SELECT * FROM users WHERE likes=:likes", {'likes': current_user.user_id})
    # cur.execute("SELECT * FROM users WHERE likes LIKE likes=:likes", {'likes': current_user.user_id})
    cur.execute("SELECT * FROM likes WHERE likes.user_id=:currentuser", {'currentuser': current_user.user_id})
    users_liked = cur.fetchall()
    print('Likes BY Current user:            ', users_liked)
    cur.execute("SELECT likes.liked_user, likes.user_id, users.username, users.image_file_p FROM likes, users WHERE likes.liked_user=:currentuser AND likes.user_id=users.user_id", {'currentuser': current_user.user_id})
    users_likedby = cur.fetchall()
    print('Likes FROM Users -> Current user: ', users_likedby)

    true_likes = []
    for index, like in enumerate(users_liked):
        try:
            if like[1] == users_likedby[index][1]:
                true_likes.append(users_likedby[index])
        except IndexError:
            pass
    
    # user_images = []
    # for user in users:
    #     image_file = url_for('static', filename='profile_pics/' + user[12])
    #     user_images.append(image_file)
    conn.close()
    return render_template('inbox.html', title='Inbox', users=true_likes) #user_images=user_images)

@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    form = MessagesForm()
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE messages.user_id=:currentuser", {'currentuser': current_user.user_id})
    messages = cur.fetchall()
    conn.close()
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        Ts = timedelta(hours = 0, minutes = 0, seconds = 0)
        timenow = datetime.now()
        Ts += timedelta(hours=timenow.hour, minutes=timenow.minute, seconds=timenow.second)
        message = Message('id', 'recipient', form.message_content.data, date.today(), str(Ts)[:-3], current_user.user_id)
        create_message(conn, cur, message)
        conn.close()
        flash('Sent!', 'success')
        return redirect(url_for('messages'))
    return render_template('messages.html', title='Messages', form=form, messages=messages)