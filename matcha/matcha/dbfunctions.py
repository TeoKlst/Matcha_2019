from matcha import sql
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from matcha import app

# None added
# def register_user(conn, cur, user):
#     with conn:
#         cur.execute("INSERT INTO users VALUES (:user_id, :firstname, :lastname, :username, :email, :password, :age, :birthdate, :gender, :sexual_pref, :biography, :famerating, :image_file, :userchecks, :tags)", 
#                     {'user_id': None, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'email': user.email, 
#                     'password': user.password, 'age': user.age, 'birthdate': user.birthdate, 'gender': user.gender, 'sexual_pref': None, 
#                     'biography': None, 'famerating': None, 'image_file': None, 'userchecks': None, 'tags': None})

# TODO Possible SQL injection vulnerability

def add_fame_like(conn, cur, user_id):
    with conn:
        cur.execute("""SELECT famerating FROM users WHERE user_id=:user_id""",
                                                        {'user_id': user_id})
        famerating = cur.fetchone()
        cur.execute("""UPDATE users SET famerating=:famerating
                WHERE user_id=:user_id""", {'famerating': (int(famerating[0]) + 5), 'user_id': user_id})

def add_fame_match(conn, cur, user_id, current_user_id):
    with conn:
        cur.execute("""SELECT famerating FROM users WHERE user_id=:user_id""",
                                                            {'user_id': user_id})
        famerating_user_id = cur.fetchone()
        cur.execute("""UPDATE users SET famerating=:famerating
                WHERE user_id=:user_id""", {'famerating': (int(famerating_user_id[0]) + 5), 'user_id': user_id})

        cur.execute("""SELECT famerating FROM users WHERE user_id=:user_id""",
                                                            {'user_id': current_user_id})
        famerating_current_user_id = cur.fetchone()
        cur.execute("""UPDATE users SET famerating=:famerating
                WHERE user_id=:user_id""", {'famerating': (int(famerating_current_user_id[0]) + 5), 'user_id': current_user_id})
        

def minus_fame_unlike(conn, cur, user_id):
    with conn:
        cur.execute("""SELECT famerating FROM users WHERE user_id=:user_id""",
                                                        {'user_id': user_id})
        famerating = cur.fetchone()
        cur.execute("""UPDATE users SET famerating=:famerating
                WHERE user_id=:user_id""", {'famerating': (int(famerating[0]) - 5), 'user_id': user_id})

def minus_fame_unmatch(conn, cur, user_id, current_user_id):
   with conn:
        cur.execute("""SELECT famerating FROM users WHERE user_id=:user_id""",
                                                            {'user_id': user_id})
        famerating_user_id = cur.fetchone()
        cur.execute("""UPDATE users SET famerating=:famerating
                WHERE user_id=:user_id""", {'famerating': (int(famerating_user_id[0]) - 10), 'user_id': user_id})

        cur.execute("""SELECT famerating FROM users WHERE user_id=:user_id""",
                                                            {'user_id': current_user_id})
        famerating_current_user_id = cur.fetchone()
        cur.execute("""UPDATE users SET famerating=:famerating
                WHERE user_id=:user_id""", {'famerating': (int(famerating_current_user_id[0]) - 5), 'user_id': current_user_id})

# TODO If there is time
def minus_fame_reported(conn, cur, user_id, current_user_id):
    pass

def register_userTest(conn, cur, user):
    with conn:
        cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, age, birthdate, gender) 
                VALUES (?,?,?,?,?,?,?,?)""",(user.firstname, user.lastname, user.username, user.email, user.password, user.age, user.birthdate, user.gender) )

def update_last_seen(conn, cur, date_time, current_user_id):
    with conn:
        cur.execute("""UPDATE users SET last_seen=:last_seen
                WHERE user_id=:user_id""", {'last_seen': date_time, 'user_id': current_user_id})

def check_like_status(conn, cur, user_id, current_user_id):
    with conn:
        cur.execute("""SELECT * FROM likes WHERE liked_user=:liked_user
                    AND user_id=:user_id""", {'liked_user': current_user_id, 'user_id': user_id})
        likee = cur.fetchone()
        cur.execute("""SELECT * FROM likes WHERE liked_user=:liked_user
                    AND user_id=:user_id""", {'liked_user': user_id, 'user_id': current_user_id})
        liked = cur.fetchone()
    if likee:
        return ('likee')
    elif liked:
        return ('liked')
    else:
        return(False)

def check_match(conn, cur, user_id, current_user_id):
    with conn:
        cur.execute("""SELECT * FROM likes WHERE liked_user=:liked_user
                    AND user_id=:user_id""", {'liked_user': current_user_id, 'user_id': user_id})
        liked = cur.fetchone()
        cur.execute("""SELECT * FROM likes WHERE liked_user=:liked_user
                    AND user_id=:user_id""", {'liked_user': user_id, 'user_id': current_user_id})
        likee = cur.fetchone()
    if not liked:
        return (False)
    if not likee:
        return (False)
    if liked[1] == likee[2]:
        return (True)
    else:
        return(False)

def update_message_notification(conn, cur, updated_message, user_id, current_user_id):
    with conn:
        cur.execute("""UPDATE message_notifications SET new_messages=:new_messages
                    WHERE last_seen_user_id=:last_seen_user_id AND user_id=:user_id
                    """, {'new_messages': updated_message, 'last_seen_user_id': user_id, 'user_id': current_user_id})

def create_message_notification(conn, cur, user_id, current_user_id):
    with conn:
        cur.execute("""INSERT INTO message_notifications (last_seen_user_id, user_id)
                    VALUES (?,?)""", (user_id, current_user_id))
        cur.execute("""INSERT INTO message_notifications (last_seen_user_id, user_id)
                    VALUES (?,?)""", (current_user_id, user_id))

def create_block(conn, cur, blocked_user, current_user_id):
    with conn:
        cur.execute("""INSERT INTO blocks (user_blocked, user_id)
                    VALUES (?,?)""", (blocked_user, current_user_id))

def get_reset_token(user_id, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')


def verify_reset_token(conn, cur, token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    cur.execute("""SELECT user_id FROM users WHERE user_id=:user_id""", {'user_id': user_id})
    user = cur.fetchone()
    return user

def create_like(conn, cur, liked, likee):
    with conn:
        cur.execute("""INSERT INTO likes (liked_user, user_id)
                    VALUES (?,?)""",(liked, likee))

def remove_like(conn, cur, liked, likee):
    with conn:
        cur.execute("DELETE FROM likes WHERE liked_user=:liked AND user_id=:likee",{'liked':liked, 'likee':likee})

def create_view(conn, cur, viewed_user, user_id):
    with conn:
        cur.execute("""INSERT INTO userviews (viewed_user, user_id)
                    VALUES (?,?)""",(viewed_user, user_id))

def save_location(conn, cur, user_id, location):
    with conn:
        cur.execute("""UPDATE users SET location_city=:city, location_region=:region, lat_data=:lat_data, long_data=:long_data
        WHERE user_id=:user_id""", {'city': location['location']['country'], 'region': location['location']['city'], 'lat_data': location['location']['lat'], 'long_data': location['location']['lng'], 'user_id': user_id})

def register_userTags(conn, cur, user_id):
    with conn:
        cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', user_id) )
        cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', user_id) )
        cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', user_id) )
        cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', user_id) )
        cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', user_id) )

def update_user(conn, cur, user):
    with conn:
        cur.execute("""UPDATE users SET firstname=:firstname, lastname=:lastname, username=:username, email=:email,
                    gender=:gender, biography=:biography, sexual_pref=:sexual_pref, geo_track=:geo_track
                    WHERE email=:email""",
                    {'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'email': user.email, 'gender': user.gender, 'biography': user.biography, 'sexual_pref': user.sexual_pref, 'geo_track': user.geo_track})

def update_tag(conn, cur, user_id, tag1cont, tag2cont, tag3cont, tag4cont, tag5cont):
    cur.execute("""SELECT * FROM tags WHERE user_id=:user_id""", {'user_id': user_id})
    user_tags = cur.fetchall()
    with conn:
        cur.execute("""UPDATE tags SET content=:content
                    WHERE id=:tag_id""",
                    {'tag_id': user_tags[0][0], 'content': tag1cont})
        cur.execute("""UPDATE tags SET content=:content
                    WHERE id=:tag_id""",
                    {'tag_id': user_tags[1][0], 'content': tag2cont})
        cur.execute("""UPDATE tags SET content=:content
                    WHERE id=:tag_id""",
                    {'tag_id': user_tags[2][0], 'content': tag3cont})
        cur.execute("""UPDATE tags SET content=:content
                    WHERE id=:tag_id""",
                    {'tag_id': user_tags[3][0], 'content': tag4cont})
        cur.execute("""UPDATE tags SET content=:content
                    WHERE id=:tag_id""",
                    {'tag_id': user_tags[4][0], 'content': tag5cont})


def update_image(conn, cur, user, img_type, img):
    if img_type == 'image_file_p':      # - p -
        cur.execute("""UPDATE users SET email=:email, 'image_file_p'=:img
                    WHERE email=:email""",
                    {'email': user.email, 'img': img})
    elif img_type == 'image_file_1':    # - 1 -
        cur.execute("""UPDATE users SET email=:email, 'image_file_1'=:img
                    WHERE email=:email""",
                    {'email': user.email, 'img': img})
    elif img_type == 'image_file_2':    # - 2 -
        cur.execute("""UPDATE users SET email=:email, 'image_file_2'=:img
                    WHERE email=:email""",
                    {'email': user.email, 'img': img})
    elif img_type == 'image_file_3':    # - 3 -
        cur.execute("""UPDATE users SET email=:email, 'image_file_3'=:img
                    WHERE email=:email""",
                    {'email': user.email, 'img': img})
    elif img_type == 'image_file_4':    # - 4 -
        cur.execute("""UPDATE users SET email=:email, 'image_file_4'=:img
                    WHERE email=:email""",
                    {'email': user.email, 'img': img})
    elif img_type == 'image_file_5':    # - 5 -
        cur.execute("""UPDATE users SET email=:email, 'image_file_5'=:img
                    WHERE email=:email""",
                    {'email': user.email, 'img': img})

def create_message(conn, cur, message):
    with conn:
        cur.execute("""INSERT INTO messages (recipient, content, date, time, user_id) 
                VALUES (?,?,?,?,?)""",(message.recipient, message.content, message.date, message.time, message.user_id) )
