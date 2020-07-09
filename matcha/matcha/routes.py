import os, re
import secrets
import requests
import geopy.distance
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, json, jsonify, session
from matcha import app, bcrypt, sql, geoKey, mail
from matcha.forms import RegistrationForm, LoginForm, UpdateAccountForm, \
                        MessagesForm, SearchForm, RequestResetForm, ResetPasswordForm, \
                        SortForm   
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message as flask_message
from datetime import date, timedelta, datetime
from collections import Counter
# Templating engine that flask uses is Jinja2
from matcha.classes import User, Message
from matcha.dbfunctions import register_userTest, update_user, update_image,\
                                create_message, register_userTags, update_tag, \
                                create_like, remove_like, create_view, save_location, \
                                get_reset_token, verify_reset_token, create_block, \
                                create_message_notification, check_match, update_message_notification, \
                                update_last_seen, check_like_status, add_fame_like, add_fame_match, \
                                minus_fame_unlike, minus_fame_unmatch, minus_fame_reported, \
                                get_authentication_token, check_user, block_check, \
                                minus_fame_block, delete_message_notification, delete_messages, \
                                save_true_location


@app.route('/')
@app.route('/home')
def home():
    users = []
    if current_user.is_authenticated:
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        cur.execute("""SELECT user_id, username, image_file_p, gender, sexual_pref, famerating, lat_data, long_data FROM users 
                                WHERE (user_id IS NOT ?)""", (str(current_user.user_id),))
        users = cur.fetchall()
        print (current_user.is_authenticated)

        cur.execute("""SELECT user_blocked FROM blocks WHERE user_id=:user_id""",
                                                        {'user_id': current_user.user_id})
        blocked_users = cur.fetchall()
        for user in blocked_users:
            i = 0
            while i < len(users):
                if user[0] == users[i][0]:
                    users.pop(i)
                i = i + 1

        # Adding distance from current user to other users
        users_with_loc = []
        current_user_latlong = [current_user.lat_data, current_user.long_data]
        for user in users:
            data = list(user)
            if user[6] is None or user[7] is None:
                distance = ''
            else:
                distance = geopy.distance.distance(current_user_latlong, (user[6], user[7]))
            if not distance:
                distance = 0
            if distance != 0:
                data.insert(8, str(distance)[:-16])
            else:
                data.insert(8, str(distance))
            data = tuple(data)
            users_with_loc.append(data)

        filtered_users_loc = []
        for user in users_with_loc:
            if int(user[8]) < 1000:
                filtered_users_loc.append(user)

        filtered_users_sexual_pref = []
        for user in filtered_users_loc:
            if current_user.sexual_pref == 'o' or not current_user.sexual_pref:
                if user[4] == current_user.gender:
                    filtered_users_sexual_pref.append(user)
                if user[4] == 'o' or not user[4]:
                    filtered_users_sexual_pref.append(user)
            elif current_user.sexual_pref == 'm':
                if user[3] == 'm' and user[4] == current_user.gender:
                    filtered_users_sexual_pref.append(user)
                if user[3] == 'm' and (user[4] == 'o' or not user[4]):
                    filtered_users_sexual_pref.append(user)
            elif current_user.sexual_pref == 'f':
                if user[3] == 'f' and user[4] == current_user.gender:
                    filtered_users_sexual_pref.append(user)
                elif user[3] == 'f' and (user[4] == 'o' or not user[4]):
                    filtered_users_sexual_pref.append(user)

        filtered_users_tags = []
        cur.execute("""SELECT * FROM tags WHERE (user_id IS ?) AND (content IS NOT ?)""", (current_user.user_id, '0'))
        current_user_tags = cur.fetchall()
        for user in filtered_users_sexual_pref:
            cur.execute("""SELECT * FROM tags WHERE (user_id IS ?) AND (content IS NOT ?)""", (user[0], '0'))
            other_user_tags = cur.fetchall()
            points = 0
            for tag in other_user_tags:
                i = 0
                while i < len(current_user_tags):
                    if tag[1] == current_user_tags[i][1]:
                        points = points + 10
                        break
                    i = i + 1
            data = list(user)
            data.insert(9, points)
            data = tuple(data)
            filtered_users_tags.append(data)

        filtered_user_fame = []
        for user in filtered_users_tags:
            fame_points = 200 - user[5]
            data = list(user)
            data.insert(10, fame_points)
            data = tuple(data)
            filtered_user_fame.append(data)

        total_user_points = []
        for user in filtered_user_fame:
            fame_points = user[10]
            tags_points = user[9]
            total_points= fame_points + tags_points
            data = list(user)
            data.insert(11, int(total_points))
            data = tuple(data)
            total_user_points.append(data)

        def getKey(item):
            return item[11]
        users = sorted(total_user_points, key=getKey, reverse=True)
        session['matched_users'] = users
        print ('MATCHED USERS: ',users)
        conn.close()
    return render_template('home.html', users=users)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    form = UpdateAccountForm()
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    if not check_user(conn, cur, username, current_user.username):
        flash('Unable to access', 'danger')
        return redirect(url_for('home'))
    cur.execute("SELECT * FROM users WHERE username=:username", {'username': username})
    user = cur.fetchone()
    userClass = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                user[7], user[8], user[9], user[10], user[11], user[12], user[13],
                user[14], user[15], user[16], user[17], user[18],
                user[19], user[20], user[21], user[22], user[23], user[24])
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

    # User View Creation on Profile Inspect
    cur.execute("SELECT * FROM userviews WHERE viewed_user=:viewed_user AND user_id=:user_id", \
                {'viewed_user': userClass.user_id, 'user_id': current_user.user_id })
    view_check = cur.fetchone()

    if not view_check:
        create_view(conn, cur, userClass.user_id, current_user.user_id)

    # cur.execute("SELECT * FROM userviews")
    # test = cur.fetchall()
    # print('ALL USERVIEWS: ',test)

    user_relation = []
    if check_match(conn, cur, userClass.user_id, current_user.user_id):
        user_relation = 'matched'
    else:
        user_relation = check_like_status(conn, cur, userClass.user_id, current_user.user_id)
    
    conn.close()
    return render_template('userprofile.html', title='User Profile', form=form, user=userClass, images=images, user_relation=user_relation)


@app.route('/views')
@login_required
def views():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userviews WHERE viewed_user=:current_user", {'current_user': current_user.user_id})
    userviews = cur.fetchall()
    userData1 = []
    for user in userviews:
        cur.execute("SELECT username, image_file_p FROM users WHERE user_id=:user_id", {'user_id': user[2]})
        data = cur.fetchone()
        if data:
            data = list(data)
            data.insert(0, user[2])
            data = tuple(data)
            userData1.append(data)

    cur.execute("SELECT * FROM userviews WHERE user_id=:current_user", {'current_user': current_user.user_id})
    viewHistory = cur.fetchall()
    userData2 = []
    for user in viewHistory:
        cur.execute("SELECT username, image_file_p FROM users WHERE user_id=:user_id", {'user_id': user[1]})
        data = cur.fetchone()
        if data:
            data = list(data)
            data.insert(0, user[2])
            data = tuple(data)
            userData2.append(data)

    view_notification = len(userData1)
    with conn:
        cur.execute("""UPDATE view_notifications SET view_notification=:view_notification
        WHERE user_id=:user_id""", {'view_notification': view_notification ,'user_id': current_user.user_id})
    conn.close
    print('USERDATA: ', userData2)
    return render_template('views.html', title='Views', userviews=userData1, viewHistory=userData2)


@app.route('/cover')
def cover():
    # print (current_user)
    return render_template('cover.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


# TODO move view_notification insert into db functions
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
                'location_region', 'lat_data', 'long_data', 'last_seen', 'authenticated')

        register_userTest(conn, cur, user)
        registered_user_ID = cur.lastrowid
        register_userTags(conn, cur, registered_user_ID)
        with conn:
            cur.execute("""INSERT INTO view_notifications (view_notification, user_id) 
                    VALUES (?,?)""",(0, registered_user_ID) )
            cur.execute("""INSERT INTO like_notifications (like_notification, user_id) 
                    VALUES (?,?)""",(0, registered_user_ID) )
        conn.close()

        send_verification_email(registered_user_ID, user)

        flash(f'Your account {form.username.data} has been created! Please verify your account through the mail to be able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


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
                    user_data[20], user_data[21], user_data[22], user_data[23], user_data[24])
    
        if user_data and bcrypt.check_password_hash(user.password, form.password.data):
            if user.authenticated == 1:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')

                # --- Geo Location ---
                cur.execute("""SELECT location_city FROM users WHERE user_id=:user_id""",
                                                    {'user_id': current_user.user_id})
                location = cur.fetchone()
                if not location[0]:
                    print ('------ LOCATION API RUNNING ------')
                    http    = 'https://ip-geolocation.whoisxmlapi.com/api/v1?'
                    json_request = requests.get('https://api.ipify.org?format=json').json()
                    ip      = json_request['ip']
                    ipAdress= 'ipAddress=' + ip
                    json_request = requests.get(http + geoKey + ipAdress).json()
                    data  = (json_request)
                    save_location(conn, cur, current_user.user_id, data)
                # --- Geo Location ---

                # --- TO BE COMMENTED IN FOR MARKING, PROOF OF GEO LOCATION WHEN GEO TURNED OFF ---
                # API call cap is bad :(
                # print ('------ TRUE LOCATION API RUNNING ------')
                # http    = 'https://ip-geolocation.whoisxmlapi.com/api/v1?'
                # json_request = requests.get('https://api.ipify.org?format=json').json()
                # ip      = json_request['ip']
                # ipAdress= 'ipAddress=' + ip
                # json_request = requests.get(http + geoKey + ipAdress).json()
                # data  = (json_request)
                # save_true_location(conn, cur, current_user.user_id, data)
                # cur.execute("""SELECT * FROM locations WHERE user_id=:user_id""",
                #                                     {'user_id': current_user.user_id})
                # location = cur.fetchone()
                # print ('TRUE CURRENT USER LOCATION: ', location)
                # --- TO BE COMMENTED IN FOR MARKING, PROOF OF GEO LOCATION WHEN GEO TURNED OFF ---
                

                conn.close()
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f'Login Unsuccessful. Please authenticate your account via registered email', 'danger')
        else:
            conn.close()
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
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()

    # LOCATION DATA
    cur.execute("""SELECT location_region FROM users WHERE user_id""")
    location_data = cur.fetchall()
    array_location = []
    for loc in location_data:
        array_location.append(loc[0])
    seen = set()
    unique = []
    for x in array_location:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    list_tuple_location = [(location, location) for location in unique]
    form.location.choices = list_tuple_location
    # LOCATION DATA

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
                form.location.data, 'lat_data', 'long_data', 'last_seen', 'authenticated')
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
        form.location.data      = current_user.location_region
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


def message_notifications(conn, cur, user_id, current_user):
    cur.execute("""SELECT new_messages FROM message_notifications 
                WHERE last_seen_user_id=:last_seen_user_id""", {'last_seen_user_id': user_id})
    new_messages = cur.fetchone()
    cur.execute("""SELECT id FROM messages 
                WHERE recipient=:recipient AND user_id=:user_id""", {'recipient': current_user, 'user_id': user_id})
    all_messages = len(cur.fetchall())
    if all_messages is None:
        all_messages = 0
    message_notif = all_messages - new_messages[0] if all_messages > new_messages[0] else new_messages[0] - all_messages 
    return (message_notif)


def append_to_tuple(tuple_data, data_to_append):
    tuple_data = list(tuple_data)
    print ('TUPLE DATA', tuple_data)
    tuple_data.insert(4, data_to_append)
    print ('TUPLE DATA AFTER APPEND', tuple_data)
    tuple_data = tuple(tuple_data)
    return (tuple_data)


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
                        notification = message_notifications(conn, cur, users_likedby[i][1], current_user.user_id)
                        new_data = append_to_tuple(users_likedby[i], notification)
                        true_likes.append(new_data)
                        break
                    i = i + 1
    print('True Likes, visible users!      : ', true_likes)
    conn.close()
    return render_template('inbox.html', title='Inbox', users=true_likes) #user_images=user_images)


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
    if not check_match(conn, cur, user_id, current_user.user_id):
        flash('Unable to access', 'danger')
        return redirect(url_for('home'))
    # Current_User
    cur.execute("SELECT * FROM messages WHERE user_id=:currentuser AND recipient=:recipient", {'currentuser': current_user.user_id, 'recipient': user_id})
    messages1 = cur.fetchall()
    # Other_User
    cur.execute("SELECT * FROM messages WHERE messages.user_id=:seconduser AND messages.recipient=:currentuser", {'seconduser': user_id, 'currentuser': current_user.user_id})
    messages2 = cur.fetchall()
    print ('messages from clicked user', len(messages2))
    update_message_notification(conn, cur, len(messages2), user_id, current_user.user_id)
    cur.execute("SELECT image_file_p, username, user_id FROM users WHERE user_id=:seconduser", {'seconduser': user_id})
    seconduser_data = cur.fetchone()
    conn.close()
    messages1 = messages1 if messages1 else [(None, None, '. . .', None, '', None)]
    messages2 = messages2 if messages2 else [(None, current_user.user_id, '. . .', None, '', None)]

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


@app.route('/likes', methods=['GET', 'POST'])
@login_required
def likes():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT likes.id, likes.liked_user, likes.user_id, users.username, users.image_file_p FROM likes, users WHERE likes.user_id=:currentuser AND likes.liked_user=users.user_id", {'currentuser': current_user.user_id})
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

    cur.execute("SELECT liked_user FROM likes WHERE liked_user=:currentuser", {'currentuser': current_user.user_id})
    like_notification = len(cur.fetchall())
    with conn:
        cur.execute("""UPDATE like_notifications SET like_notification=:like_notification
        WHERE user_id=:user_id""", {'like_notification': like_notification ,'user_id': current_user.user_id})
    conn.close()
    return render_template('likes.html', title='Likes', matched_users=true_likes,
    currentuser_unmatched_likes=currentuser_unmatched_likes, otheruser_unmatched_likes=otheruser_unmatched_likes)


@app.route('/like_func/<string:user_id>', methods=['GET', 'POST'])
def likes_func(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("""SELECT image_file_p FROM users WHERE user_id=:user_id""",
                                                        {'user_id': current_user.user_id})
    profile_img_check = cur.fetchone()
    if profile_img_check[0] != "default.jpg":
        if not block_check(conn, cur, user_id, current_user.user_id):
            create_like(conn, cur, user_id, current_user.user_id)
            add_fame_like(conn, cur, user_id)
            if check_match(conn, cur, user_id, current_user.user_id):
                add_fame_match(conn, cur, user_id, current_user.user_id)
                cur.execute("""SELECT * FROM message_notifications WHERE last_seen_user_id=:last_seen_user_id
                        AND user_id=:user_id""", {'last_seen_user_id': current_user.user_id, 'user_id': user_id})
                all_message_notifs = cur.fetchall()
                if not all_message_notifs:
                    create_message_notification(conn, cur, user_id, current_user.user_id)
            conn.close()
            flash('Like Successful!', 'success')
            return render_template('home.html', title='Views')
        else:
            flash('You have blocked or been blocked by this user, unable to like.', 'danger')
            return render_template('home.html', title='Home')
    else:
        flash('Your profile picture is still the deafult. Please go to your account info to update.', 'warning')
        return render_template('home.html', title='Home')


@app.route('/unlike_func/<string:user_id>', methods=['GET','POST'])
def unlike_func(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    if check_match(conn, cur, user_id, current_user.user_id):
        minus_fame_unmatch(conn, cur, user_id, current_user.user_id)
    else:
        minus_fame_unlike(conn, cur, user_id)
    remove_like(conn, cur, user_id, current_user.user_id)
    conn.close()
    flash('User Unliked!', 'warning')
    return render_template('home.html', title='Views')


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
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    
    cur.execute("""SELECT location_region FROM users WHERE user_id""")
    location_data = cur.fetchall()

    array_location = []
    for loc in location_data:
        array_location.append(loc[0])

    seen = set()
    unique = []
    for x in array_location:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    unique.insert(0, 'Choose Location')

    list_tuple_location = [(location, location) for location in unique]
    form.location.choices = list_tuple_location
    conn.close()

    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()

        age_min = form.age_min.data
        age_max = form.age_max.data

        fame_min = form.fame_rating_min.data
        fame_max = form.fame_rating_max.data

        location = form.location.data

        tag1 = form.tag1.data
        tag2 = form.tag2.data
        tag3 = form.tag3.data
        tag4 = form.tag4.data
        tag5 = form.tag5.data

        # AGE
        found_age_users = []
        if age_min != '0' or age_max != '0':
            min_check = False
            max_check = False

            if age_min != '0':
                min_check = True
            if age_max != '0':
                max_check = True

            if min_check and max_check:
                # SEARCH FROM A TO B
                cur.execute("""SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)""",
                                                        (int(age_min), int(age_max)))
                found_age_users = cur.fetchall()
            elif min_check:
                # SEARCH FROM LOWEST TO HIGHEST
                cur.execute("""SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)""",
                                                        (int(age_min), 100))
                found_age_users = cur.fetchall()
            elif max_check:
                # SEARCH HIGHEST TO LOWEST
                cur.execute("""SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)""",
                                                        (0, int(age_max)))
                found_age_users = cur.fetchall()
            
            # Checks if valid user was found, if none fails search criteria
            if not found_age_users:
                found_age_users = False

        # FAME
        found_fame_users = []
        if fame_min != '0' or fame_max != '0':
            min_check = False
            max_check = False

            if fame_min != '0':
                min_check = True
            if fame_max != '0':
                max_check = True

            if min_check and max_check:
                # SEARCH FROM A TO B
                cur.execute("""SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)""",
                                                        (int(fame_min), int(fame_max)))
                found_fame_users = cur.fetchall()
            elif min_check:
                # SEARCH FROM LOWEST TO HIGHEST
                cur.execute("""SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)""",
                                                        (int(fame_min), 200))
                found_fame_users = cur.fetchall()
            elif max_check:
                # SEARCH HIGHEST TO LOWEST
                cur.execute("""SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)""",
                                                        (0, int(fame_max)))
                found_fame_users = cur.fetchall()

            # Checks if valid user was found, if none fails search criteria
            if not found_fame_users:
                found_fame_users = False

        # LOCATION
        found_location_users = []
        if location != 'Choose Location':
            cur.execute("""SELECT user_id FROM users WHERE location_region=:location_region""",
                                                        {'location_region': location})
            found_location_users = cur.fetchall()

        # TAG
        found_tags_users = []
        if tag1 != '0' or tag2 != '0' or tag3 != '0' or tag4 != '0' or tag5 != '0':

            tag_list = []
            if tag1 != '0':
                tag_list.append(tag1)
            if tag2 != '0':
                tag_list.append(tag2)
            if tag3 != '0':
                tag_list.append(tag3)
            if tag4 != '0':
                tag_list.append(tag4)
            if tag5 != '0':
                tag_list.append(tag5)

            tag_list_len = len(tag_list)

            if tag_list_len == 1:
                cur.execute("""SELECT user_id FROM tags WHERE content=:content1""",
                                                        {'content1': tag_list[0]})
                found_tags_users = cur.fetchall()
            elif tag_list_len == 2:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?)""", 
                                                        (tag_list[0], tag_list[1]))
                found_tags_users = cur.fetchall()
            elif tag_list_len == 3:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?, ?)""",
                                                        (tag_list[0], tag_list[1], tag_list[2]))
                found_tags_users = cur.fetchall()
            elif tag_list_len == 4:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?, ?, ?)""",
                                                        (tag_list[0], tag_list[1], tag_list[2], tag_list[3]))
                found_tags_users = cur.fetchall()
            elif tag_list_len == 5:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?, ?, ?, ?)""",
                                                        (tag_list[0], tag_list[1], tag_list[2], tag_list[3], tag_list[4]))
                found_tags_users = cur.fetchall()

            # Checks if valid user was found, if none fails search criteria
            if not found_tags_users:
                found_tags_users = False
            else:
                if found_tags_users:
                    temp_list1 = []
                    for user in found_tags_users:
                        temp_list1.append(user[0])

                    counted = Counter(temp_list1)
                    temp_list2 = []
                    for x in counted:
                        if int(counted[x]) == tag_list_len:
                            temp_list2.append(x)
                    found_tags_users = temp_list2

                    if not found_tags_users:
                        found_tags_users = False


        # found_tags_users = tuple([user] for user in found_tags_users)
        # print ('ALL USERS FOUND IN TAGS: ', found_tags_users)
        cur.execute("SELECT user_id FROM users WHERE (user_id IS NOT ?)", (str(current_user.user_id),))
        # cur.execute("SELECT user_id FROM users WHERE user_id")
        all_users = cur.fetchall()

        # Remove blocked users
        cur.execute("""SELECT user_blocked FROM blocks WHERE user_id=:user_id""",
                                                        {'user_id': current_user.user_id})
        blocked_users = cur.fetchall()
        for user in blocked_users:
            i = 0
            while i < len(all_users):
                if user[0] == all_users[i][0]:
                    all_users.pop(i)
                i = i + 1

        filtered_users = []
        filtered_age = []
        if found_age_users:
            for index, user in enumerate(found_age_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_age.append(user)
                        break
                    i = i + 1
        if filtered_age:
            filtered_users = filtered_age
            all_users = filtered_users

        filtered_fame = []
        if found_fame_users:
            for index, user in enumerate(found_fame_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_fame.append(user)
                        break
                    i = i + 1
        if filtered_fame:
            filtered_users = filtered_fame
            all_users = filtered_users

        filtered_location = []
        if found_location_users:
            for index, user in enumerate(found_location_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_location.append(user)
                        break
                    i = i + 1
        if filtered_location:
            filtered_users = filtered_location
            all_users = filtered_users
            # print ('FILTERED LOCATION: ',found_location_users)

        filtered_tags = []
        if found_tags_users:
            for index, user in enumerate(found_tags_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i][0]:
                        filtered_tags.append(user)
                        break
                    i = i + 1
            if not filtered_tags:
                found_tags_users = False 
        if filtered_tags:
            filtered_users = filtered_tags
            all_users = filtered_users

        # print ('FILTERED USER CRITERIA AFTER AGE, FAME, TAGS CHECK: ',found_tags_users)

        # SEARCH FOR MATCHING USERS
        if found_age_users == False or found_fame_users == False or found_tags_users == False or not filtered_users:
            flash('No users found!', 'warning')
            return redirect(url_for('search'))
        else:
            flash('Validated!', 'success')
            session['found_users'] = filtered_users
            return redirect(url_for('search_results'))
    elif request.method == 'GET':
        pass
    return render_template('search.html', title='Search', form=form)


@app.route('/search_results', methods=['GET', 'POST'])
@login_required
def search_results():
    form = SortForm()
    found_users = session.get('found_users', None)
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()

    cur.execute("""SELECT lat_data, long_data FROM users WHERE user_id=:user_id""",
                                                        {'user_id': current_user.user_id})
    user_latlong = cur.fetchone()

    check_is = True
    try:
        test = found_users[0][0]
    except TypeError:
        check_is = False

    filtered_users_data = []
    if check_is == False:
        for user in found_users:
            cur.execute("""SELECT user_id, username, image_file_p, age, famerating, location_city, location_region, lat_data, long_data 
                            FROM users WHERE user_id=:user_id""", {'user_id': user})
            user_data = cur.fetchone()
            cur.execute("""SELECT user_id, content FROM tags WHERE user_id=:user_id""",
                                                                {'user_id': user})
            tag_data = cur.fetchall()
            valid_tags = 0
            for tag in tag_data:
                if tag[1] != '0':
                    valid_tags = valid_tags + 1

            user_distance = geopy.distance.distance(user_latlong, (user_data[7], user_data[8]))
            if not user_distance:
                user_distance = 0
            data = list(user_data)
            data.insert(5, valid_tags)
            if user_distance != 0:
                data.insert(6, str(user_distance)[:-16])
            else:
                 data.insert(6, str(user_distance))
            data = tuple(data)
            filtered_users_data.append(data)
    else:
        for user in found_users:
            cur.execute("""SELECT user_id, username, image_file_p, age, famerating, location_city, location_region, lat_data, long_data 
                            FROM users WHERE user_id=:user_id""", {'user_id': user[0]})
            user_data = cur.fetchone()
            cur.execute("""SELECT user_id, content FROM tags WHERE user_id=:user_id""",
                                                                {'user_id': user[0]})
            tag_data = cur.fetchall()
            valid_tags = 0
            # print (tag_data)
            for tag in tag_data:
                if tag[1] != '0':
                    valid_tags = valid_tags + 1

            user_distance = geopy.distance.distance(user_latlong, (user_data[7], user_data[8]))
            if not user_distance:
                user_distance = 0
            data = list(user_data)
            data.insert(5, valid_tags)
            if user_distance != 0:
                data.insert(6, str(user_distance)[:-16])
            else:
                 data.insert(6, str(user_distance))
            data = tuple(data)
            filtered_users_data.append(data)

    # print ('FILTERED DATA WITH TAGS APPEND: ',filtered_users_data)
    session['matched_users'] = filtered_users_data

    if request.method == 'POST' and form.validate():
        form_select = form.field_select.data
        form_sort = form.type_sort.data
        
        if form_select != '0' and form_sort != '0':
            sorted_users = filtered_users_data
            type_sort = True if form_sort == 'desc' else False
            kind_sort = []
            if form_select == 'age':
                kind_sort = 3
            elif form_select == 'fame':
                kind_sort = 4
            elif form_select == 'tags':
                kind_sort = 5
            elif form_select == 'location':
                kind_sort = 6
        
            # Sorting Tuple
            def getKey(item):
                return item[kind_sort]
            sorted_users = sorted(sorted_users, key=getKey, reverse=type_sort)
 
            flash('Sorted!', 'success')
            session['sorted_users'] = sorted_users
            return redirect(url_for('sort_results'))
        else:
            flash('Please select sort criteria!', 'warning')
            return redirect(url_for('search_results'))

    return render_template('search_results.html', title='Search Result', form=form, users=filtered_users_data)


@app.route('/sort_results', methods=['GET', 'POST'])
@login_required
def sort_results():
    sorted_users = session.get('sorted_users', None)
    print ('-----------------',sorted_users)
    return render_template('sort_results.html', title='Sort Result', users=sorted_users)


@app.route('/block_user/<user_id>', methods=['GET', 'POST'])
def block_user(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    # create block for current_user
    create_block(conn, cur, user_id, current_user.user_id)
    # create block for blocked user
    create_block(conn, cur, current_user.user_id, user_id)
    # remove user_id like
    remove_like(conn, cur, user_id, current_user.user_id)
    # remove current_user like
    remove_like(conn, cur, current_user.user_id, user_id)
    # remove fame
    minus_fame_block(conn, cur, user_id, current_user.user_id)
    # delete notifications
    delete_message_notification(conn, cur, user_id, current_user.user_id)
    # delete all messages
    delete_messages(conn, cur, user_id, current_user.user_id)
    conn.close()
    flash('User has been blocked', 'danger')
    return redirect(url_for('home'))


@app.route('/report_user/<username>', methods=['GET', 'POST'])
def report_user(username):
    send_report_email(username, current_user.email)
    flash('User has been reported, an email has been sent to log the report.', 'danger')
    return redirect(url_for('home'))


def send_verification_email(user_id, user):
    token = get_authentication_token(user_id)
    # print (token)
    msg = flask_message('Account Authentication', 
                    sender='noreply@matcha.com', 
                    recipients=[user.email])
    msg.body = f'''To authenticate your account, visit the following link:
{url_for('authentication_token', token=token, _external=True)}

'''
    mail.send(msg)


@app.route('/authentication_token/<token>', methods=['GET', 'POST'])
def authentication_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    user = verify_reset_token(conn, cur, token)
    conn.close()
    if not user:
        flash('That is an invalid or expired token, please re-register', 'warning')
        return redirect(url_for('register'))
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""UPDATE users SET authenticated=:authenticated
                    WHERE user_id=:token_id""",
                    {'token_id': user[0], 'authenticated': 1})
    conn.close()
    flash('Account authenticated!', 'success')
    return redirect(url_for('login'))


def send_report_email(reported_user, current_user):
    msg = flask_message('User Report', 
                    sender='noreply@matcha.com', 
                    recipients=[current_user])
    msg.body = f'''Thank you for your report on user:{reported_user}, we will investigate the matter.
'''
    mail.send(msg)


def send_reset_email(user):
    token = get_reset_token(user[1])
    # print (token)
    msg = flask_message('Password Reset Request', 
                    sender='noreply@matcha.com', 
                    recipients=[user[0]])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        cur.execute("SELECT email, user_id FROM users WHERE email=:email", {'email': form.email.data})
        user_data = cur.fetchone()
        # print (user_data)
        send_reset_email(user_data)
        conn.close()
        flash('An email has been sent with instructions to reset you password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    user = verify_reset_token(conn, cur, token)
    conn.close()
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()
        print (form.password_field.data)
        print (user[0])
        hashed_password = bcrypt.generate_password_hash(form.password_field.data).decode('utf-8')
        with conn:
            cur.execute("""UPDATE users SET password=:new_password
                        WHERE user_id=:token_id""",
                        {'token_id': user[0], 'new_password': hashed_password})
        conn.close()
        flash('Password updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/inbox_notifications')
def inbox_notifications():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT new_messages FROM message_notifications WHERE user_id=:user_id", {'user_id': current_user.user_id})
    notification = cur.fetchall()
    cur.execute("SELECT * FROM messages WHERE recipient=:recipient", {'recipient': current_user.user_id})
    all_messages = len(cur.fetchall())
    conn.close()
    total_notes = 0
    for note in notification:
        total_notes = total_notes + note[0]
    if total_notes is None:
        total_notes = 0
    message_notification = all_messages - total_notes if all_messages > total_notes else total_notes - all_messages
    return jsonify({'inbox': message_notification})


@app.route('/like_notifications')
def like_notifications():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM likes WHERE liked_user=:liked_user""", {'liked_user': current_user.user_id})
    likes_to_user = len(cur.fetchall())
    cur.execute("""SELECT like_notification FROM like_notifications WHERE user_id=:user_id""", {'user_id': current_user.user_id})
    notification = cur.fetchone()
    conn.close()
    like_notification = likes_to_user - notification[0] if likes_to_user > notification[0] else notification[0] - likes_to_user
    return jsonify({'likes': like_notification})


@app.route('/view_notifications')
def view_notifications():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("""SELECT view_notification FROM view_notifications where user_id=:user_id""", {'user_id': current_user.user_id})
    last_viewed = cur.fetchone()
    cur.execute("""SELECT * FROM userviews where viewed_user=:viewed_user""", {'viewed_user': current_user.user_id})
    total_views = len(cur.fetchall())
    conn.close()
    view_notification = total_views - last_viewed[0] if total_views > last_viewed[0] else last_viewed[0] - total_views
    return jsonify({'views': view_notification})


@app.route('/realtime_chat/<user_id>')
def realtime_chat(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM messages WHERE recipient=:recipient AND user_id=:user_id"""
                , {'recipient': current_user.user_id, 'user_id': user_id})
    other_user_message = cur.fetchall()
    cur.execute("""SELECT new_messages FROM message_notifications WHERE last_seen_user_id=:last_seen_user_id AND user_id=:user_id"""
                , {'last_seen_user_id': user_id, 'user_id': current_user.user_id})
    new_messages = cur.fetchone()
    len_other_messages = len(other_user_message)
    message = []
    if len_other_messages > new_messages[0]:
        update_message_notification(conn, cur, len_other_messages, user_id, current_user.user_id)
        ranges =  len_other_messages - (len_other_messages - new_messages[0])
        for x in range(ranges, (len_other_messages)):
            message.append(other_user_message[x])
            update = 'True'
        return jsonify({'message'   : '<div class="mb-1 text-right"><small class="text-muted pull-left">' + message[0][4][:-3] + '</small>' + \
                                      '<button type="button" class="btn btn-info">' + message[0][2] + '</button><br></div>',
                        'update'    : update})
    update = 'False'
    return jsonify({'message'   : '<div class="mb-1 text-right"><small class="text-muted pull-left">' + 'TIME DATA' + '</small>' + \
                                  '<button type="button" class="btn btn-info">' + 'MESSAGE CONTENT' + '</button><br></div>',
                    'update'    : update })


@app.route('/last_seen_set')
def last_seen_set():
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    current_time = datetime.now()

    Ts = timedelta(hours = 0, minutes = 0, seconds = 0)
    timenow = datetime.now()
    Ts += timedelta(hours=timenow.hour, minutes=timenow.minute, seconds=timenow.second)
    time_now = str(Ts)
    date_now = date.today()
    time_check = Ts + timedelta(minutes=5)
    info = str(date_now) + ' ' + time_now

    update_last_seen(conn, cur, current_time, current_user.user_id)
    return jsonify({})


@app.route('/last_seen_load/<user_id>')
def last_seen_load(user_id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("""SELECT last_seen FROM users WHERE user_id=:user_id""",
                {'user_id': user_id})
    last_seen = cur.fetchone()
    Ts = timedelta(hours = 0, minutes = 0, seconds = 0)
    timenow = datetime.now()
    Ts += timedelta(hours=timenow.hour, minutes=timenow.minute, seconds=timenow.second)
    Ts -= timedelta(seconds=5)
    # print ('LAST SEEN:',last_seen)
    if last_seen[0] is None:
        return jsonify({'last_seen_time'   : ''})
    else:
        split1 = last_seen[0].split(' ') 
        split2 = split1[1].split(':')
        convert_time = timedelta(hours = int(split2[0]), minutes = int(split2[1]), seconds = int(split2[2][:-7]))
        if (convert_time > Ts):
            return jsonify({'last_seen_time'   : '<p class="text-success">' + 'Online' + '</p>'})
        else:
            return jsonify({'last_seen_time'   : last_seen[0][:-10]})


# =============================================================== END DATA ===============================================================


@app.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    form = SearchForm()
    matched_users = session.get('matched_users', None)
    print ('+++++++++++++', matched_users)

    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    
    cur.execute("""SELECT location_region FROM users WHERE user_id""")
    location_data = cur.fetchall()

    array_location = []
    for loc in location_data:
        array_location.append(loc[0])

    seen = set()
    unique = []
    for x in array_location:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    unique.insert(0, 'Choose Location')

    list_tuple_location = [(location, location) for location in unique]
    form.location.choices = list_tuple_location
    conn.close()

    if form.validate_on_submit():
        conn = sql.connect('matcha\\users.db')
        cur = conn.cursor()

        age_min = form.age_min.data
        age_max = form.age_max.data

        fame_min = form.fame_rating_min.data
        fame_max = form.fame_rating_max.data

        location = form.location.data

        tag1 = form.tag1.data
        tag2 = form.tag2.data
        tag3 = form.tag3.data
        tag4 = form.tag4.data
        tag5 = form.tag5.data

        # AGE
        found_age_users = []
        if age_min != '0' or age_max != '0':
            min_check = False
            max_check = False

            if age_min != '0':
                min_check = True
            if age_max != '0':
                max_check = True

            if min_check and max_check:
                # SEARCH FROM A TO B
                cur.execute("""SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)""",
                                                        (int(age_min), int(age_max)))
                found_age_users = cur.fetchall()
            elif min_check:
                # SEARCH FROM LOWEST TO HIGHEST
                cur.execute("""SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)""",
                                                        (int(age_min), 100))
                found_age_users = cur.fetchall()
            elif max_check:
                # SEARCH HIGHEST TO LOWEST
                cur.execute("""SELECT user_id FROM users WHERE (age BETWEEN ? AND ?)""",
                                                        (0, int(age_max)))
                found_age_users = cur.fetchall()
            
            # Checks if valid user was found, if none fails search criteria
            if not found_age_users:
                found_age_users = False

        # FAME
        found_fame_users = []
        if fame_min != '0' or fame_max != '0':
            min_check = False
            max_check = False

            if fame_min != '0':
                min_check = True
            if fame_max != '0':
                max_check = True

            if min_check and max_check:
                # SEARCH FROM A TO B
                cur.execute("""SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)""",
                                                        (int(fame_min), int(fame_max)))
                found_fame_users = cur.fetchall()
            elif min_check:
                # SEARCH FROM LOWEST TO HIGHEST
                cur.execute("""SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)""",
                                                        (int(fame_min), 200))
                found_fame_users = cur.fetchall()
            elif max_check:
                # SEARCH HIGHEST TO LOWEST
                cur.execute("""SELECT user_id FROM users WHERE (famerating BETWEEN ? AND ?)""",
                                                        (0, int(fame_max)))
                found_fame_users = cur.fetchall()

            # Checks if valid user was found, if none fails search criteria
            if not found_fame_users:
                found_fame_users = False

        # LOCATION
        found_location_users = []
        if location != 'Choose Location':
            cur.execute("""SELECT user_id FROM users WHERE location_region=:location_region""",
                                                        {'location_region': location})
            found_location_users = cur.fetchall()

        # TAG
        found_tags_users = []
        if tag1 != '0' or tag2 != '0' or tag3 != '0' or tag4 != '0' or tag5 != '0':

            tag_list = []
            if tag1 != '0':
                tag_list.append(tag1)
            if tag2 != '0':
                tag_list.append(tag2)
            if tag3 != '0':
                tag_list.append(tag3)
            if tag4 != '0':
                tag_list.append(tag4)
            if tag5 != '0':
                tag_list.append(tag5)

            tag_list_len = len(tag_list)

            if tag_list_len == 1:
                cur.execute("""SELECT user_id FROM tags WHERE content=:content1""",
                                                        {'content1': tag_list[0]})
                found_tags_users = cur.fetchall()
            elif tag_list_len == 2:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?)""", 
                                                        (tag_list[0], tag_list[1]))
                found_tags_users = cur.fetchall()
            elif tag_list_len == 3:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?, ?)""",
                                                        (tag_list[0], tag_list[1], tag_list[2]))
                found_tags_users = cur.fetchall()
            elif tag_list_len == 4:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?, ?, ?)""",
                                                        (tag_list[0], tag_list[1], tag_list[2], tag_list[3]))
                found_tags_users = cur.fetchall()
            elif tag_list_len == 5:
                cur.execute("""SELECT user_id FROM tags WHERE content IN (?, ?, ?, ?, ?)""",
                                                        (tag_list[0], tag_list[1], tag_list[2], tag_list[3], tag_list[4]))
                found_tags_users = cur.fetchall()

            # Checks if valid user was found, if none fails search criteria
            if not found_tags_users:
                found_tags_users = False
            else:
                if found_tags_users:
                    temp_list1 = []
                    for user in found_tags_users:
                        temp_list1.append(user[0])

                    counted = Counter(temp_list1)
                    temp_list2 = []
                    for x in counted:
                        if int(counted[x]) == tag_list_len:
                            temp_list2.append(x)
                    found_tags_users = temp_list2

                    if not found_tags_users:
                        found_tags_users = False

        # found_tags_users = tuple([user] for user in found_tags_users)
        # print ('ALL USERS FOUND IN TAGS: ', found_tags_users)
        all_users = []
        for user in matched_users:
            cur.execute("SELECT user_id FROM users WHERE (user_id IS ?)", (user[0],))
            user_id = cur.fetchone()
            all_users.append(user_id)
        print ('--------------', all_users)
        filtered_users = []

        filtered_age = []
        if found_age_users:
            for index, user in enumerate(found_age_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_age.append(user)
                        break
                    i = i + 1
        if filtered_age:
            filtered_users = filtered_age
            all_users = filtered_users

        filtered_fame = []
        if found_fame_users:
            for index, user in enumerate(found_fame_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_fame.append(user)
                        break
                    i = i + 1
        if filtered_fame:
            filtered_users = filtered_fame
            all_users = filtered_users

        filtered_location = []
        if found_location_users:
            for index, user in enumerate(found_location_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i]:
                        filtered_location.append(user)
                        break
                    i = i + 1
        if filtered_location:
            filtered_users = filtered_location
            all_users = filtered_users
            # print ('FILTERED LOCATION: ',found_location_users)

        filtered_tags = []
        if found_tags_users:
            for index, user in enumerate(found_tags_users):
                i = 0
                while i != len(all_users):
                    if user == all_users[i][0]:
                        filtered_tags.append(user)
                        break
                    i = i + 1
            if not filtered_tags:
                found_tags_users = False 
        if filtered_tags:
            filtered_users = filtered_tags
            all_users = filtered_users

        # print ('FILTERED USER CRITERIA AFTER AGE, FAME, TAGS CHECK: ',found_tags_users)

        # SEARCH FOR MATCHING USERS
        if found_age_users == False or found_fame_users == False or found_tags_users == False or not filtered_users:
            flash('No users found!', 'warning')
            return redirect(url_for('home'))
        else:
            flash('Validated!', 'success')
            session['found_users'] = filtered_users
            return redirect(url_for('search_results'))
    elif request.method == 'GET':
        pass
    return render_template('filter.html', title='Filter', form=form, users=matched_users)


@app.route('/sort', methods=['GET', 'POST'])
@login_required
def sort():
    form = SortForm()
    found_users = session.get('matched_users', None)
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()

    cur.execute("""SELECT lat_data, long_data FROM users WHERE user_id=:user_id""",
                                                        {'user_id': current_user.user_id})
    user_latlong = cur.fetchone()

    check_is = True
    try:
        test = found_users[0][0]
    except TypeError:
        check_is = False

    filtered_users_data = []
    if check_is == False:
        for user in found_users:
            cur.execute("""SELECT user_id, username, image_file_p, age, famerating, location_city, location_region, lat_data, long_data 
                            FROM users WHERE user_id=:user_id""", {'user_id': user})
            user_data = cur.fetchone()
            cur.execute("""SELECT user_id, content FROM tags WHERE user_id=:user_id""",
                                                                {'user_id': user})
            tag_data = cur.fetchall()
            valid_tags = 0
            for tag in tag_data:
                if tag[1] != '0':
                    valid_tags = valid_tags + 1

            user_distance = geopy.distance.distance(user_latlong, (user_data[7], user_data[8]))
            if not user_distance:
                user_distance = 0
            data = list(user_data)
            data.insert(5, valid_tags)
            if user_distance != 0:
                data.insert(6, str(user_distance)[:-16])
            else:
                 data.insert(6, str(user_distance))
            data = tuple(data)
            filtered_users_data.append(data)
    else:
        for user in found_users:
            cur.execute("""SELECT user_id, username, image_file_p, age, famerating, location_city, location_region, lat_data, long_data 
                            FROM users WHERE user_id=:user_id""", {'user_id': user[0]})
            user_data = cur.fetchone()
            cur.execute("""SELECT user_id, content FROM tags WHERE user_id=:user_id""",
                                                                {'user_id': user[0]})
            tag_data = cur.fetchall()
            valid_tags = 0
            # print (tag_data)
            for tag in tag_data:
                if tag[1] != '0':
                    valid_tags = valid_tags + 1

            user_distance = geopy.distance.distance(user_latlong, (user_data[7], user_data[8]))
            if not user_distance:
                user_distance = 0
            data = list(user_data)
            data.insert(5, valid_tags)
            if user_distance != 0:
                data.insert(6, str(user_distance)[:-16])
            else:
                 data.insert(6, str(user_distance))
            data = tuple(data)
            filtered_users_data.append(data)

    # print ('FILTERED DATA WITH TAGS APPEND: ',filtered_users_data)
    session['matched_users'] = filtered_users_data

    if request.method == 'POST' and form.validate():
        form_select = form.field_select.data
        form_sort = form.type_sort.data
        
        if form_select != '0' and form_sort != '0':
            sorted_users = filtered_users_data
            type_sort = True if form_sort == 'desc' else False
            kind_sort = []
            if form_select == 'age':
                kind_sort = 3
            elif form_select == 'fame':
                kind_sort = 4
            elif form_select == 'tags':
                kind_sort = 5
            elif form_select == 'location':
                kind_sort = 6
        
            # Sorting Tuple
            def getKey(item):
                return item[kind_sort]
            sorted_users = sorted(sorted_users, key=getKey, reverse=type_sort)
 
            flash('Sorted!', 'success')
            session['sorted_users'] = sorted_users
            return redirect(url_for('sort_results'))
        else:
            flash('Please select sort criteria!', 'warning')
            return redirect(url_for('sort'))

    return render_template('sort.html', title='Sort', form=form, users=filtered_users_data)


# ------------------------------------------ ERROR PAGE HANDLING ------------------------------------------

@app.errorhandler(403) 
def error_403(error): 
    return render_template('errors/403.html')

@app.errorhandler(404) 
def error_404(error): 
    return render_template('errors/404.html')

@app.errorhandler(500) 
def error_500(error): 
    return render_template('errors/500.html')
