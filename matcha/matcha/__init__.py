import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = '02f223f600f6e93454be89fb8ec9c78c'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# SQLAlchemy database instance
# Represent database structure as classes/models
# Each class will be a table in the database
geoKey = 'apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&'
sql = sqlite3
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chamatch101@gmail.com'
app.config['MAIL_PASSWORD'] = 'JamesJameson123'
mail = Mail(app)


from matcha import routes

# Sectret Key Generation $> secrets.token_hex(16)
# Helps to protect from modifying cookies and cross-site request forgery attacks. 