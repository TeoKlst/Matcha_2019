class User:

    def __init__(self, user_id, firstname, lastname, age, birthdate,
                username, email, password, gender, sexual_pref,
                biography, famerating, image_file_p, image_file_1, 
                image_file_2, image_file_3, image_file_4, image_file_5,
                geo_track, location_city, location_region, lat_data, long_data,
                last_seen):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.birthdate = birthdate
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.sexual_pref = sexual_pref
        self.biography = biography
        self.famerating = famerating
        self.image_file_p = image_file_p
        self.image_file_1 = image_file_1
        self.image_file_2 = image_file_2
        self.image_file_3 = image_file_3
        self.image_file_4 = image_file_4
        self.image_file_5 = image_file_5
        self.geo_track = geo_track
        self.location_city = location_city
        self.location_region = location_region
        self.lat_data = lat_data
        self.long_data = long_data
        self. last_seen = last_seen

        

    def get_id(self):
        return (self.user_id)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    # @property
    # def email(self):
    #     return '{}.{}@email.com'.format(self.first, self.last)

    # @property
    # def fullname(self):
    #     return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "User('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
        self.user_id, self.firstname, self.lastname, self.age, self.birthdate,
        self.username, self.email, self.password, self.gender, self.sexual_pref,
        self.biography, self.famerating, self.image_file_p, self.image_file_1,
        self.image_file_2, self.image_file_3, self.image_file_4, self.image_file_5,
        self.geo_track, self.location_city, self.location_region, self.lat_data,
        self.long_data, self.last_seen)

class RegisterUser:
    pass

class Message:
    def __init__(self, id, recipient, content, date, time, user_id):
        self.id = id
        self.recipient = recipient
        self.content = content
        self.date = date
        self.time = time
        self.user_id = user_id
    
    def __repr__(self):
        return "User('{}', '{}', '{}', '{}', '{}', '{}')".format(
        self.id, self.recipient, self.content, self.date, self.time, self.user_id)