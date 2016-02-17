import datetime
from flask.ext.login import UserMixin
from app import app, db, login_manager, bcrypt
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    is_email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    country_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    date_joined = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    votes = db.relationship('Vote', backref='user', lazy='dynamic')
    otp = db.relationship('OTP', backref='user', lazy='dynamic')
    token = db.relationship('Token', backref='user', lazy='dynamic')

    def __init__(self, country_code, phone, is_admin=False,
                is_email_confirmed=False):
        self.country_code = country_code
        self.phone = phone
        self.date_joined = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
        self.is_admin = is_admin
        self.is_email_confirmed = is_email_confirmed

    def __repr__(self):
        return '<User (name={}, password={}, email={}, mobile={})>'.format(
                self.name, self.password, self.email, self.mobile)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class OTP(db.Model):
    __tablename__ = 'otps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    otp_type = db.Column(db.String)
    otp_num = db.Column(db.Integer, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    attempt = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, otp_num, expires_at, user_id, otp_type='sms'):
        self.otp_num = otp_num
        self.expires_at = expires_at
        self.otp_type = otp_type
        self.user_id = user_id

    def __repr__(self):
        return '<OTP (otp={}, expires_at={}, user_id={})>'.formate(self.otp,
                self.expires_at, self.user_id)



class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, token, expires_at, user_id):
        self.token = token
        self.expires_at = expires_at
        self.user_id = user_id

    def __repr__(self):
        return '<Token (token={}, expires_at={}, user_id={})>'.formate(
                self.token, self.expires_at, self.user_id)


class Mosque(db.Model):
    __tablename__ = 'mosques'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    imam_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topics = db.relationship('Topic', backref='mosque', lazy='dynamic')
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, name, country, latitude, longitude, is_active=False):
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.date_added = datetime.datetime.now()
        self.is_active = is_active

    def __repr__(self):
        return '<Mosque (name={})>'.format(self.name)


class MosqueThing(db.Model):
    __tablename__ = 'mosque_things'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thing = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosques.id'))

    def __init__(self, thing, value, mosque_id):
        self.thing = thing
        self.value = value
        self.mosque_id = mosque_id

    def __repr__(self):
        return '<MosqueThing (thing={}, value={}, mosque_id={})>'.format(
            self.thing, self.value, self.mosque_id)


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vote_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, topic_id, user_id):
        self.topic_id = topic_id
        self.user_id = user_id
        self.vote_date = datetime.datetime.now()

    def __repr__(self):
        return '<Vote (topic={})>'.format(self.topic_id)


class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosques.id'))
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime, nullable=False)
    votes = db.relationship('Vote', backref='topic', lazy='dynamic')
    # statuses: new, ignore, future
    status = db.Column(db.String)

    def __init__(self, title, description, user_created_id, mosque_id, status='new'):
        self.title = title
        self.description = description
        self.user_created_id=user_created_id
        self.mosque_id = mosque_id
        self.date_added = datetime.datetime.now()
        self.status = status

    def __repr__(self):
        return '<Topic (title={})>'.format(self.title)


class Khutbah(db.Model):
    __tablename__ = 'khutbahs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosques.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    date = db.Column(db.DateTime, nullable=False)
    is_enforced = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, mosque_id, topic_id, date, is_enforced=False):
        self.mosque_id = mosque_id
        self.topic_id = topic_id
        self.date = date
        self.is_enforced = is_enforced

    def __repr__(self):
        return '<Khutbah (mosque_id={}, topic_id={})>'.format(self.mosque_id,
                self.topic_id)


if __name__ == '__main__':
    manager.run()
