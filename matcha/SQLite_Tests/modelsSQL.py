import sqlite3

conn = sqlite3.connect('users.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            age INTEGER,
            birthdate TEXT,
            username TEXT,
            email TEXT,
            password TEXT,
            gender TEXT,
            sexual_pref TEXT,
            biography TEXT,
            famerating INTEGER,
            image_file TEXT DEFAULT "default.jpg" NOT NULL,
            userchecks INTEGER,
            tags TEXT
            """)

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