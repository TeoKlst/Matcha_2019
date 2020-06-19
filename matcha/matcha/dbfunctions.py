from matcha import sql
# None added
def register_user(conn, cur, user):
    with conn:
        cur.execute("INSERT INTO users VALUES (:user_id, :firstname, :lastname, :username, :email, :password, :age, :birthdate, :gender, :sexual_pref, :biography, :famerating, :image_file, :userchecks, :tags)", 
                    {'user_id': None, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'email': user.email, 
                    'password': user.password, 'age': user.age, 'birthdate': user.birthdate, 'gender': user.gender, 'sexual_pref': None, 
                    'biography': None, 'famerating': None, 'image_file': None, 'userchecks': None, 'tags': None})

# TODO Possible SQL injection vulnerability
def register_userTest(conn, cur, user):
    with conn:
        cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",(user.firstname, user.lastname, user.username, user.email, user.password, user.age, user.birthdate, user.gender) )