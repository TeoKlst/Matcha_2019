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
        cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",(user.firstname, user.lastname, user.username, user.email, user.password, user.age, user.birthdate, user.gender) )

def update_user(conn, cur, user):
    with conn:
        cur.execute("""UPDATE users SET firstname=:firstname, lastname=:lastname, username=:username, email=:email, gender=:gender, biography=:biography
                    WHERE email=:email""",
                    {'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'email': user.email, 'gender': user.gender, 'biography': user.biography})

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

