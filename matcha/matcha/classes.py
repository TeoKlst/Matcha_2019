class User:

    def __init__(self, user_id, firstname, lastname, age, birthdate,
                username, email, password, gender, sexual_pref,
                biography, famerating, image_file_p, image_file_1, 
                image_file_2, image_file_3, image_file_4, image_file_5, 
                userchecks, tags):
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
        self.userchecks = userchecks
        self.tags = tags

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
        return "User('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {})".format(
        self.user_id, self.firstname, self.lastname, self.age, self.birthdate,
        self.username, self.email, self.password, self.gender, self.sexual_pref,
        self.biography, self.famerating, self.image_file_p, self.image_file_1,
        self.image_file_2, self.image_file_3, self.image_file_4, self.image_file_5, 
        self.userchecks, self.tags)

class RegisterUser:
    pass