import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from matcha import app, bcrypt, sql
from matcha.forms import RegistrationForm, LoginForm, UpdateAccountForm, MessagesForm, SearchForm
# from matcha.models import Like, Message, Images, Tags, Post    
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, timedelta, datetime

# Templating engine that flask uses is Jinja2
db = 1
from matcha.classes import User, Message
from matcha.dbfunctions import register_userTest, update_user, update_image, create_message, register_userTags, update_tag, create_like, remove_like

postsMass = [
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
    },
    {
    },
        {
    },
        {
    },
        {
    },
        {
    },
        {
    },
        {
    },
        {
    },
]

@app.route('/')
@app.route('/home')
def home():
    posts = postsMass
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id")
    users = cur.fetchall()
    print (current_user.is_authenticated)
    conn.close()
    return render_template('home.html', posts=posts, users=users)

@app.route('/user/<username>', methods=['GET', 'POST'])
def user_profile(username):
    form = UpdateAccountForm()
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=:username", {'username': username})
    user = cur.fetchone()
    userClass = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                user[7], user[8], user[9], user[10], user[11], user[12], user[13],
                user[14], user[15], user[16], user[17], user[18],
                user[19], user[20])
    print ('++++++++++++++++++++++++++++++++++++ User Data=>',userClass)
    form.firstname.data     = userClass.firstname
    form.lastname.data      = userClass.lastname
    form.username.data      = userClass.username
    form.email.data         = userClass.email
    form.gender.data        = userClass.gender
    form.sexual_pref.data   = userClass.sexual_pref
    form.biography.data     = userClass.biography
    form.geo_tag.data       = userClass.geo_track
    cur.execute("SELECT * FROM tags WHERE user_id=:user_id", {'user_id': userClass.user_id})
    tags = cur.fetchall()
    form.user_tag1.data = tags[0][1]
    form.user_tag2.data = tags[1][1]
    form.user_tag3.data = tags[2][1]
    form.user_tag4.data = tags[3][1]
    form.user_tag5.data = tags[4][1]
    image_file_p = url_for('static', filename='profile_pics/' + userClass.image_file_p)
    image_file_1 = url_for('static', filename='profile_pics/' + userClass.image_file_1) if userClass.image_file_1 else None
    image_file_2 = url_for('static', filename='profile_pics/' + userClass.image_file_2) if userClass.image_file_2 else None
    image_file_3 = url_for('static', filename='profile_pics/' + userClass.image_file_3) if userClass.image_file_3 else None
    image_file_4 = url_for('static', filename='profile_pics/' + userClass.image_file_4) if userClass.image_file_4 else None
    image_file_5 = url_for('static', filename='profile_pics/' + userClass.image_file_5) if userClass.image_file_5 else None
    images = [image_file_1, image_file_2, image_file_3, image_file_4, image_file_5]

    # cur.execute("SELECT * FROM likes WHERE liked_user=:user_id AND user_id=:current_user", {'user_id': userClass.user_id, 'current_user': current_user.user_id})
    # likes = cur.fetchone()
    conn.close()
    return render_template('userprofile.html', title='User Profile', form=form, user=userClass, images=images)

@app.route('/cover')
def cover():
    # print (current_user)
    return render_template('cover.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

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
                'image_file_3', 'image_file_4', 'image_file_5', 'geo_track', 'location_city',
                'location_region')

        register_userTest(conn, cur, user)
        registered_user_ID = cur.lastrowid
        register_userTags(conn, cur, registered_user_ID)
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
                    user_data[15], user_data[16], user_data[17], user_data[18], user_data[19],
                    user_data[20])

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
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    if form.validate_on_submit():
        # ------ Images ------
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
        # ------ User ------
        user = User('user_id', form.firstname.data, form.lastname.data, 'age', 'birthdate',
                form.username.data, form.email.data, 'hashed_password', form.gender.data, form.sexual_pref.data,
                form.biography.data, 'famerating', 'image_file_p', 'image_file_1', 'image_file_2',
                'image_file_3', 'image_file_4', 'image_file_5', form.geo_tag.data, 'location_city',
                'location_region')
        update_user(conn, cur, user)
        # ------ Tags ------
        update_tag(conn, cur, current_user.user_id, form.user_tag1.data, form.user_tag2.data, form.user_tag3.data, form.user_tag4.data, form.user_tag5.data)

        conn.close()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data     = current_user.firstname
        form.lastname.data      = current_user.lastname
        form.username.data      = current_user.username
        form.email.data         = current_user.email
        form.gender.data        = current_user.gender
        form.sexual_pref.data   = current_user.sexual_pref
        form.biography.data     = current_user.biography
        form.geo_tag.data       = current_user.geo_track
        cur.execute("SELECT * FROM tags WHERE user_id=:user_id", {'user_id': current_user.user_id})
        tags = cur.fetchall()
        form.user_tag1.data = tags[0][1]
        form.user_tag2.data = tags[1][1]
        form.user_tag3.data = tags[2][1]
        form.user_tag4.data = tags[3][1]
        form.user_tag5.data = tags[4][1]
        conn.close()
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
                i = 0
                while i != len(users_likedby):
                    if like[1] == users_likedby[i][1]:
                        true_likes.append(users_likedby[i])
                        break
                    i = i + 1
    print('True Likes, visible users!      : ', true_likes)
    conn.close()
    return render_template('inbox.html', title='Inbox', users=true_likes) #user_images=user_images)

# TODO Sort by date 1st, then within date sections sort by time
# TODO Clean data passing (messages1 & 2)???
# Null message add user_id so it can be split
@app.route('/messages/<user_id>', methods=['GET', 'POST'])
@login_required
def messages(user_id):
    # true_likes = request.args.get('true_likes')
    # print('+++++++++++++++++++++++++++', true_likes)
    # checker = True
    # for like in true_likes:
    #     if user_id == like[0]:
    #         checker = None
    # if checker:
    #     abort(403)
    form = MessagesForm()
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    # Current_User
    cur.execute("SELECT * FROM messages WHERE user_id=:currentuser AND recipient=:recipient", {'currentuser': current_user.user_id, 'recipient': user_id})
    messages1 = cur.fetchall()
    # Other_User
    cur.execute("SELECT * FROM messages WHERE messages.user_id=:seconduser AND messages.recipient=:currentuser", {'seconduser': user_id, 'currentuser': current_user.user_id})
    messages2 = cur.fetchall()
    cur.execute("SELECT image_file_p, username FROM users WHERE user_id=:seconduser", {'seconduser': user_id})
    seconduser_data = cur.fetchone()
    conn.close()
    messages1 = messages1 if messages1 else [(None, None, '. . .', None, '', None)]
    messages2 = messages2 if messages2 else [(None, None, '. . .', None, '', None)]

    messages3 = []
    messages3 = messages1 + messages2
    # Sorting Tuple
    def getKey(item):
        return item[4]
    messages3 = sorted(messages3, key=getKey)
    # print ('================= messages 3 =====================',messages3)
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        Ts = timedelta(hours = 0, minutes = 0, seconds = 0)
        timenow = datetime.now()
        Ts += timedelta(hours=timenow.hour, minutes=timenow.minute, seconds=timenow.second)
        message = Message('id', user_id , form.message_content.data, date.today(), str(Ts), current_user.user_id)
        create_message(conn, cur, message)
        conn.close()
        flash('Sent!', 'success')
        return redirect(url_for('messages', user_id=user_id))
    return render_template('messages.html', title='Messages', form=form, messages1=messages1, messages2=messages2, seconduser_data=seconduser_data, messages3=messages3)

# Get image data from current_user like -> another_user. So if the other user hasn't liked back.
@app.route('/likes', methods=['GET', 'POST'])
@login_required
def likes():
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
    
    # Matching current_user likes against all
    true_likes = []
    currentuser_unmatched_likes = []
    for index, like in enumerate(users_liked):
        i = 0
        while i != len(users_likedby):
            if like[1] == users_likedby[i][1]:
                true_likes.append(users_likedby[i])
                break
            i = i + 1
        try:
            if like[1] != true_likes[len(true_likes) - 1][1]:
                currentuser_unmatched_likes.append(like)
        except IndexError:
            currentuser_unmatched_likes.append(like)
    print('True Likes, visible users!      : ', true_likes)
    print('UserOnlyLikes,haventliked!      : ', currentuser_unmatched_likes)
    
    # STOPPED HERE
    # Matching other users likes again current_user
    otheruser_unmatched_likes = []
    for index, like in enumerate(users_likedby):
        i = 0
        check = None
        while i != len(users_liked):
            if like[1] == users_liked[i][1]:
                check = True
            i = i + 1 
        if not check:
            otheruser_unmatched_likes.append(like)
    print('UNMAETCHEDlikesofotherUsers    :', otheruser_unmatched_likes)
    conn.close()
    return render_template('likes.html', title='Likes', matched_users=true_likes,
    currentuser_unmatched_likes=currentuser_unmatched_likes, otheruser_unmatched_likes=otheruser_unmatched_likes)


@app.route('/like_func/<string:user_id>', methods=['GET', 'POST'])
def likes_func(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    create_like(conn, cur, user_id, current_user.user_id)
    flash('Like Successful!', 'success')
    return render_template('home.html', title='Views')


@app.route('/unlike_func/<string:user_id>', methods=['GET','POST'])
def unlike_func(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    remove_like(conn, cur, user_id, current_user.user_id)
    flash('User Unliked!', 'warning')
    return render_template('home.html', title='Views')


@app.route('/views')
def views():
    return render_template('views.html', title='Views')

# legend="Name" can be used to be passed to other routes to change naming {{ legend }}
# To add a action to a button
# <form action="{{ url_for('unlike', user_id=user.id) }}" method="POST">
#   <input class="btn btn-danger" type="submit" value="Delete">
# </form>
# @app.route('/messages/<user_id>/unlike', methods=['POST'])
# @login_required
# def unlike(user_id):
#     pass

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()

        age_gap = form.age.data
        fame_gap = form.fame_rating.data

        if age_gap != '0':
            upA = (int(age_gap) + current_user.age)
            lowA= (int(age_gap) - current_user.age) if int(age_gap) > current_user.age else (current_user.age - int(age_gap))
            # print (upA)
            # print (lowA)
            cur.execute("SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)", (lowA, upA))
            found_age_users = cur.fetchall()

        if fame_gap != '0':
            upF = (int(fame_gap) + current_user.famerating)
            lowF= (int(fame_gap) - current_user.famerating) if int(fame_gap) > current_user.famerating else (current_user.famerating - int(fame_gap))
            # print ('Fame',upF)
            # print ('Fame',lowF)
            cur.execute("SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)", (lowF, upF))
            found_fame_users = cur.fetchall()

        # -------------------> WIP
        # if location != '0':
            # pass
        # if tags != '0':
            # pass
        # -------------------> WIP

        cur.execute("SELECT user_id FROM users WHERE user_id")
        all_users = cur.fetchall()
        filtered_users = []

        filtered_users1 = []
        if age_gap != '0':
            for index, user in enumerate(found_age_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_users1.append(user)
                        break
                    i = i + 1

        filtered_users2 = []
        if fame_gap != '0':
            for index, user in enumerate(found_fame_users):
                i = 0
                while i != len(filtered_users1):
                    if user == filtered_users1[i]:
                        filtered_users2.append(user)
                        break
                    i = i + 1

        print('--------SEARCH RESULT:', filtered_users2)

        flash('Validated!', 'success')
        return redirect(url_for('search'))
    elif request.method == 'GET':
        pass
    return render_template('search.html', title='Likes', form=form)