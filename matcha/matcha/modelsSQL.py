# < ---------- Bcrypt --------- >
from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
# < ---------- Bcrypt --------- >

from datetime import datetime
import sqlite3

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @login_manager.user_loader
# def load_user(id):
#     conn = sqlite3.connect('users.db')
#     cur = conn.cursor()
#     cur.execute("SELECT username from users where username = (?)", [id])
#     userrow = cur.fetchone()
#     userid = userrow[0] # or whatever the index position is
#     return int(userid)

conn = sqlite3.connect('users.db')
# conn = sqlite3.connect(':memory:')
print ("Opened database successfully")

cur = conn.cursor()

cur.execute("""CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            age INTEGER NOT NULL,
            birthdate TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            gender TEXT NOT NULL,
            sexual_pref TEXT NULL,
            biography TEXT NULL,
            famerating INTEGER DEFAULT 100,
            image_file_p TEXT DEFAULT "default.jpg",
            image_file_1 TEXT NULL,
            image_file_2 TEXT NULL,
            image_file_3 TEXT NULL,
            image_file_4 TEXT NULL,
            image_file_5 TEXT NULL,
            geo_track TEXT DEFAULT "1",
            location_city TEXT NULL,
            location_region TEXT NULL
            )""")

cur.execute("""CREATE TABLE location (
            lat INTEGER NULL,
            long INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient INTEGER NULL,
            content TEXT NULL,
            date TEXT NULL,
            time TEXT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            liked_user INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE userviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            viewed_user INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

# =================================================================== USERS ==========================================================================
hashed_password = bcrypt.generate_password_hash('tkelest123').decode('utf-8')
# cur.execute("""INSERT INTO users VALUES (1, 'Teo', 'Kelestura', '25', '07/12/1994', 'Tkelest',
#             'tkelest@gmail.com', hashed_password, 'male', 'female', 
#             'Biography', 'Fame:1', 'default.jpg',
#             'Userchecks', 'Tags' )""")

# ------ UserID 1 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",('Teo', 'Kelestura', 'Tkelest', 'tkelest@gmail.com', hashed_password, 'm', 25, '07/12/1994') )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(2, 1) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(3, 1) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 1) )

# ------ UserID 2 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",('Maya', 'Haya', 'MayaHi', 'maya@gmail.com', hashed_password, 'f', 25, '07/12/1994') )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(1, 2) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(5, 2) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 2) )

# ------ UserID 3 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",('Jamie', 'Jameson', 'Jay', 'jayjay@gmail.com', hashed_password, 'f', 30, '07/12/1994') )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(1, 3) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(2, 3) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(4, 3) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(5, 3) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 3) )

# ------ UserID 4 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",('Brad', 'Bradson', 'BradB', 'brad@gmail.com', hashed_password, 'm', 35, '07/12/1994') )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(2, 4) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(3, 4) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 4) )

# ------ UserID 5 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate) 
                VALUES (?,?,?,?,?,?,?,?)""",('Tommy', 'Thomson', 'TheDankEngine', 'dank@gmail.com', hashed_password, 'm', 40, '07/12/1994') )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(2, 5) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(3, 5) )

cur.execute("""INSERT INTO likes (liked_user, user_id)
                VALUES (?,?)""",(4, 5) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 5) )



conn.commit()
# ================================================================= USERS END ========================================================================

# cur.execute("""SELECT messages.id, messages.recipient, messages.content, users.username
#             FROM users, messages WHERE users.user_id=messages.user_id AND users.likes=2 OR users.likes=3 """)
# cur.execute("""SELECT messages.id, messages.recipient, messages.content, users.username
#             FROM users, messages WHERE users.user_id=messages.user_id """)
# messages = cur.fetchall()
# print (messages)

# cur.execute("SELECT * FROM messages WHERE user_id=:user_id", {'user_id': 1})
# messages1 = cur.fetchall()
# print (messages1)

# cur.execute("SELECT * FROM likes WHERE id")
# messages1 = cur.fetchall()
# print (messages1)

# cur.execute("SELECT * FROM users WHERE lastname=:lastname", {'lastname':'Kelestura'})
# print(cur.fetchall())

choices_gender  =[('m', 'Male'), ('f', 'Female'), ('o', 'Other')]

choices_day     =[('0', 'Day'), 
                    ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), 
                    ('10','10'), ('11','11'), ('12','12'), ('13','13'), ('14','14'), ('15','15'), ('16','16'), ('17','17'), 
                    ('18','18'), ('19','19'), ('20','20'), ('21','21'), ('22','22'), ('23','23'), ('24','24'), ('25','25'), 
                    ('26','26'), ('27','27'), ('28','28'), ('29','29'), ('30','30'), ('31','31')]

choices_month   =[('0', 'Month'), 
                    ('1','Jan'), ('2','Feb'), ('3','Mar'), 
                    ('4','Apr'), ('5','May'), ('6','Jun'), 
                    ('7','Jul'), ('8','Aug'), ('9','Sept'), 
                    ('10','Oct'), ('11','Nov'), ('12','Dec')]

choices_year    =[('0', 'Year'), 
                    ('1987','1987'), ('1988','1988'), ('1989','1989'), ('1990','1990'), ('1991','1991'), ('1992','1992'), ('1993','1993'),
                    ('1994','1994'), ('1995','1995'), ('1996','1996'), ('1997','1997'), ('1998','1998'), ('1999','1999'), ('2000','2000'), 
                    ('2001','2001'), ('2002','2002'), ('2003','2003'), ('2004','2004'), ('2005','2005'), ('2006','2006'), ('2007','2007')]

print ("Table created successfully")
conn.close()
