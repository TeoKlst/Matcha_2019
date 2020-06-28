from matcha import sql
# None added
# def register_user(conn, cur, user):
#     with conn:
#         cur.execute("INSERT INTO users VALUES (:user_id, :firstname, :lastname, :username, :email, :password, :age, :birthdate, :gender, :sexual_pref, :biography, :famerating, :image_file, :userchecks, :tags)", 
#                     {'user_id': None, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'email': user.email, 
#                     'password': user.password, 'age': user.age, 'birthdate': user.birthdate, 'gender': user.gender, 'sexual_pref': None, 
#                     'biography': None, 'famerating': None, 'image_file': None, 'userchecks': None, 'tags': None})

# TODO Possible SQL injection vulnerability
def register_userTest(conn, cur, user):
    with conn:
        cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, age, birthdate, gender) 
                VALUES (?,?,?,?,?,?,?,?)""",(user.firstname, user.lastname, user.username, user.email, user.password, user.age, user.birthdate, user.gender) )

def create_like(conn, cur, liked, likee):
    with conn:
        cur.execute("""INSERT INTO likes (liked_user, user_id)
                    VALUES (?,?)""",(liked, likee))

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
                    gender=:gender, biography=:biography, sexual_pref=:sexual_pref, geo_track=:geo_track, location_city=:location_city,
                    location_region=:location_region
                    WHERE email=:email""",
                    {'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'email': user.email, 'gender': user.gender, 'biography': user.biography, 'sexual_pref': user.sexual_pref, 'geo_track': user.geo_track, 'location_city': user.location_city, 'location_region': user.location_region})

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
