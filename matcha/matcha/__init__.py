from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '02f223f600f6e93454be89fb8ec9c78c'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# SQLAlchemy database instance
# Represent database structure as classes/models
# Each class will be a table in the database
sql = sqlite3
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from matcha import routes

# Sectret Key Generation $> secrets.token_hex(16)
# Helps to protect from modifying cookies and cross-site request forgery attacks. 