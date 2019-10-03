from datetime import datetime
from matcha import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

choices_gender  =[('m', 'Male'), ('f', 'Female'), ('o', 'Other')]

choices_age     =[('18', '18'), ('19', '19'), ('20', '20')]

choices_day     =[('', 'Day'), ('1','1')]

choices_month   =[('', 'Month'), ('1','Jan'), ('2','Feb'), ('3','Mar'), ('4','Apr'), ('5','May'), ('6','Jun'), ('7','Jul'), ('8','Aug'), ('9','Sept'), ('10','Oct'), ('11','Nov'), ('12','Dec')]

choices_year    =[('', 'Year'), ('1994','1994')]

class User(db.Model, UserMixin):
    id          = db.Column(db.Integer, primary_key=True)
    firstname   = db.Column(db.String(20), nullable=False)
    lastname    = db.Column(db.String(20), nullable=False)
    age         = db.Column(db.String(20), nullable=False)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    password    = db.Column(db.String(60), nullable=False)
    gender      = db.Column(db.String(20), nullable=False)
    # sexualpref  = db.Column(db.String(20), nullable=False)
    # biography   = db.Column(db.Text, nullable=False)
    # famerating  = db.Column(db.Integer, nullable=False, default=0)
    # SET IN ROUTES ON ACCOUNT PAGE
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    # userchecks  = db.Column(db.String(100), default='')
    # tags        = db.Column(db.String(20), default='') 
    posts       = db.relationship('Post', backref='author', lazy=True)
    # likes       = db.relationship('Like', backref='userlikes', lazy=True)
    # messages    = db.relationship('Message', backref='usermessages', lazy=True)
    # user_images = db.relationship('Images', backref='userimages', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Like(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.id}', '{self.user_id}', '{self.username}')"

class Message(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    content     = db.Column(db.Text, nullable=False)
    date_sent   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Message('{self.content}', '{self.date_sent}', '{self.username}')"

class Images(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    # 1 = Profile photo , 2 - 5 = Being other photos
    image_rel   = db.Column(db.Integer, nullable=False)
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Message('{self.content}', '{self.date_sent}', '{self.username}')"

class Tags(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    user_list   = db.Column(db.Text, default='')

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.user_list}')"

class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content     = db.Column(db.Text, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
            return f"Post('{self.title}', '{self.date_posted}')"