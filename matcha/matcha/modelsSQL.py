# < ---------- Bcrypt --------- >
from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
# < ---------- Bcrypt --------- >
from datetime import datetime
import sqlite3


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
            location_region TEXT NULL,
            lat_data INTEGER NULL,
            long_data INTEGER NULL,
            last_seen TEXT NULL,
            authenticated INTEGER DEFAULT 0
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

cur.execute("""CREATE TABLE blocks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_blocked INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE message_notifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_seen_date TEXT NULL,
            last_seen_time TEXT NULL,
            last_seen_user_id INTEGER NULL,
            new_messages INTEGER DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE like_notifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            like_notification INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE view_notifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            view_notification INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

cur.execute("""CREATE TABLE locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_city TEXT NULL,
            location_region TEXT NULL,
            lat_data INTEGER NULL,
            long_data INTEGER NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id) 
            )""")

# =================================================================== USERS ==========================================================================
hashed_password = bcrypt.generate_password_hash('tkelest123').decode('utf-8')


# ------ UserID 1 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate, authenticated) 
                VALUES (?,?,?,?,?,?,?,?,?)""",('Teo', 'Kelestura', 'Tkelest', 'tkelest@gmail.com', hashed_password, 'm', 25, '07/12/1994', 1) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 1) )

cur.execute("""INSERT INTO view_notifications (view_notification, user_id) 
                VALUES (?,?)""",(0, 1) )

cur.execute("""INSERT INTO like_notifications (like_notification, user_id) 
                VALUES (?,?)""",(0, 1) )


# ------ UserID 2 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate, authenticated) 
                VALUES (?,?,?,?,?,?,?,?,?)""",('Maya', 'Haya', 'MayaHi', 'maya@gmail.com', hashed_password, 'f', 25, '07/12/1994', 1) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 2) )

cur.execute("""INSERT INTO view_notifications (view_notification, user_id) 
                VALUES (?,?)""",(0, 2) )

cur.execute("""INSERT INTO like_notifications (like_notification, user_id) 
                VALUES (?,?)""",(0, 2) )


# ------ UserID 3 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate, authenticated) 
                VALUES (?,?,?,?,?,?,?,?,?)""",('Jamie', 'Jameson', 'Jay', 'jayjay@gmail.com', hashed_password, 'f', 30, '07/12/1994', 1) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 3) )

cur.execute("""INSERT INTO view_notifications (view_notification, user_id) 
                VALUES (?,?)""",(0, 3) )

cur.execute("""INSERT INTO like_notifications (like_notification, user_id) 
                VALUES (?,?)""",(0, 3) )


# ------ UserID 4 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate, location_city, location_region, lat_data, long_data, authenticated) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",('Brad', 'Bradson', 'BradB', 'brad@gmail.com', hashed_password, 'm', 35, '07/12/1994', 'ITL', 'Rome', 41.898555, 12.521133, 1) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 4) )

cur.execute("""INSERT INTO view_notifications (view_notification, user_id) 
                VALUES (?,?)""",(0, 4) )

cur.execute("""INSERT INTO like_notifications (like_notification, user_id) 
                VALUES (?,?)""",(0, 4) )


# ------ UserID 5 ------
cur.execute("""INSERT INTO users (firstname, lastname, username, email, password, gender, age, birthdate, location_city, location_region, lat_data, long_data, authenticated) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",('Tommy', 'Thomson', 'TheDankEngine', 'dank@gmail.com', hashed_password, 'm', 40, '07/12/1994', 'ZA', 'Cape Town', -33.9550, 18.5859, 1) )

for i in range(5):
    cur.execute("""INSERT INTO tags (content, user_id)
                    VALUES (?,?)""",('0', 5) )

cur.execute("""INSERT INTO view_notifications (view_notification, user_id) 
                VALUES (?,?)""",(0, 5) )

cur.execute("""INSERT INTO like_notifications (like_notification, user_id) 
                VALUES (?,?)""",(0, 5) )



conn.commit()
# ================================================================= USERS END ========================================================================

print ("Table created successfully")
conn.close()
