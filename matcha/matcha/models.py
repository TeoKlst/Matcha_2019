from datetime import datetime
from matcha import login_manager, sql
from flask_login import UserMixin
from matcha.classes import User

# Test by changing id to user_id
@login_manager.user_loader
def load_user(id):
    conn = sql.connect('matcha\\users.db')
    cur = conn.cursor()
    cur.execute("SELECT * from users where email = (?)", [id])
    userrow = cur.fetchone()
    print ('id ', id)
    print ('fetchone ', userrow)
    # userid = userrow[0] # or whatever the index position is
    user = User(userrow[0], userrow[1], userrow[2], userrow[3], userrow[4],
            userrow[5], userrow[6], userrow[7], userrow[8], userrow[9],
            userrow[10], userrow[11], userrow[12], userrow[13], userrow[14], 
            userrow[15], userrow[16], userrow[17], userrow[18], userrow[19],
            userrow[20])
    print('return id', user)
    return (user)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

choices_gender  =[('m', 'Male'), ('f', 'Female'), ('o', 'Other')]

choices_sexpreference =[('m', 'Male'), ('f', 'Female'), ('o', 'Other')]

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

choices_gap     =[('0', 'Choose Range'),
                    ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10'),
                    ('11','11'), ('12','12'), ('13','13'), ('14','14'), ('15','15'), ('16','16'), ('17','17'), ('18','18'), ('19','19'),
                    ('20','20'), ('21','21'), ('22','22'), ('23','23'), ('24','24'), ('25','25'), ('26','26'), ('27','27'), ('28','28'), ('29','29'),
                    ('30','30'), ('31','31'), ('32','32'), ('33','33'), ('34','34'), ('35','35'), ('36','36'), ('37','37'), ('38','38'), ('39','39'),
                    ('40','40'), ('41','41'), ('42','42'), ('43','43'), ('44','44'), ('45','45'), ('46','46'), ('47','47'), ('48','48'), ('49','49'),
                    ('50','50'), ('51','51'), ('52','52'), ('53','53'), ('54','54'), ('55','55'), ('56','56'), ('57','57'), ('58','58'), ('59','59'),
                    ('60','60'), ('61','61'), ('62','62'), ('63','63'), ('64','64'), ('65','65'), ('66','66'), ('67','67'), ('68','68'), ('69','69'),
                    ('70','70'), ('71','71'), ('72','72'), ('73','73'), ('74','74'), ('75','75'), ('76','76'), ('77','77'), ('78','78'), ('79','79'),
                    ('80','80'), ('81','81'), ('82','82'), ('83','83'), ('84','84'), ('85','85'), ('86','86'), ('87','87'), ('88','88'), ('89','89'),
                    ('90','90'), ('91','91'), ('92','92'), ('93','93'), ('94','94'), ('95','95'), ('96','96'), ('97','97'), ('98','98'), ('99','99'),]

choices_tags    =[('0','Choose a tag...'), ('Food','Food'), ('Sports','Sports'), ('Movies','Movies'), ('Fitness','Fitness'), ('Animals','Animals'), ('Tech','Tech'), ('Art','Art'), ('Music','Music'),
                    ('Night Owl','Night Owl'), ('Early Bird','Early Bird'), ('Drinks','Drinks'), ('Reading','Reading'), ('Outdoors','Outdoors'), ('Homebody','Homebody'),
                    ('City Slicker','City Slicker'), ('Fashion','Fashion'), ('Camping','Camping'), ('Travelling','Travelling'), ('Hobby Collector','Hobby Collector'), ('Cooking','Cooking')]

choices_geo     =[('0','Off'), ('1','On')]
# class User(db.Model, UserMixin):
#     id          = db.Column(db.Integer, primary_key=True)
#     firstname   = db.Column(db.String(20), nullable=False)
#     lastname    = db.Column(db.String(20), nullable=False)
#     age         = db.Column(db.String(20), nullable=False)
#     birthdate   = db.Column(db.String(20), nullable=False)
#     username    = db.Column(db.String(20), unique=True, nullable=False)
#     email       = db.Column(db.String(120), unique=True, nullable=False)
#     password    = db.Column(db.String(60), nullable=False)
#     gender      = db.Column(db.String(20), nullable=False)
#     # +
#     sexualpref  = db.Column(db.String(20), nullable=False, default='')
#     # +
#     biography   = db.Column(db.Text, nullable=False, default='')
#     # +
#     famerating  = db.Column(db.Integer, nullable=False, default=0)
#     # Set in routes on account page
#     image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
#     # +
#     userchecks  = db.Column(db.String(100), default='')
#     # +
#     tags        = db.Column(db.String(20), default='') 
#     posts       = db.relationship('Post', backref='author', lazy=True)
#     # likes       = db.relationship('Like', backref='userlikes', lazy=True)
#     # messages    = db.relationship('Message', backref='usermessages', lazy=True)
#     # user_images = db.relationship('Images', backref='userimages', lazy=True)

#     # How the class is printed, when it is printed out
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# class Like(db.Model):
#     id          = db.Column(db.Integer, primary_key=True)
#     username    = db.Column(db.String(20), unique=True, nullable=False)
#     user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Like('{self.id}', '{self.user_id}', '{self.username}')"

# class Message(db.Model):
#     id          = db.Column(db.Integer, primary_key=True)
#     username    = db.Column(db.String(20), unique=True, nullable=False)
#     content     = db.Column(db.Text, nullable=False)
#     date_sent   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Message('{self.content}', '{self.date_sent}', '{self.username}')"

# class Images(db.Model):
#     id          = db.Column(db.Integer, primary_key=True)
#     # 1 = Profile photo , 2 - 5 = Being other photos
#     image_rel   = db.Column(db.Integer, nullable=False)
#     image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
#     user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Message('{self.content}', '{self.date_sent}', '{self.username}')"

# class Tags(db.Model):
#     id          = db.Column(db.Integer, primary_key=True)
#     title       = db.Column(db.String(100), nullable=False)
#     user_list   = db.Column(db.Text, default='')

#     def __repr__(self):
#         return f"Post('{self.id}', '{self.title}', '{self.user_list}')"

# class Post(db.Model):
#     id          = db.Column(db.Integer, primary_key=True)
#     title       = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content     = db.Column(db.Text, nullable=False)
#     user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#             return f"Post('{self.title}', '{self.date_posted}')"