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
    date_created = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    otp = db.relationship('OTP', backref='user', lazy='dynamic')

    def __init__(self, country_code, phone, is_admin=False,
                is_email_confirmed=False):
        self.country_code = country_code
        self.phone = phone
        self.date_created = datetime.datetime.now()
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


class UserThing(db.Model):
    __tablename__ = 'user_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thing = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, thing, value, user_id):
        self.thing = thing
        self.value = value
        self.user_id = user_id

    def __repr__(self):
        return '<UserThing (thing={}, value={}, user_id={})>'.format(
            self.thing, self.value, self.user_id)

class ACL(db.Model):
    __tablename__ = 'acls'


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


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, type, name, country, latitude, longitude, user_created_id):
        self.type = type
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.user_created_id = user_created_id
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return '<Place (name={})>'.format(self.name)


class PlaceThing(db.Model):
    __tablename__ = 'place_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thing = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))

    def __init__(self, thing, value, place_id):
        self.thing = thing
        self.value = value
        self.place_id = place_id

    def __repr__(self):
        return '<PlaceThing (thing={}, value={}, place_id={})>'.format(
            self.thing, self.value, self.place_id)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, nullable=False)
    articles = db.relationship('Article', backref='article', lazy='dynamic')
    things = db.relationship('ArticleThing', backref='thing', lazy='dynamic')

    def __init__(self, type, place_id, user_created_id):
        self.type = type
        self.place_id = place_id
        self.user_created_id = user_created_id
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return '<Event (place_id={}, type={})>'.format(self.place_id,
                self.type)


class EventThing(db.Model):
    __tablename__ = 'event_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thing = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __init__(self, thing, value, event_id):
        self.thing = thing
        self.value = value
        self.event_id = event_id

    def __repr__(self):
        return '<EventThing (thing={}, value={}, event_id={})>'.format(
            self.thing, self.value, self.event_id)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    plase_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, nullable=False)
    things = db.relationship('ArticleThing', backref='thing', lazy='dynamic')

    def __init__(self, type, title, description, user_created_id, plase_id):
        self.type = type
        self.title = title
        self.description = description
        self.user_created_id = user_created_id
        self.plase_id = plase_id
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return '<Article (title={})>'.format(self.title)


class ArticleThing(db.Model):
    __tablename__ = 'article_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thing = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    def __init__(self, thing, value, article_id):
        self.thing = thing
        self.value = value
        self.article_id = article_id

    def __repr__(self):
        return '<ArticleThing (thing={}, value={}, article_id={})>'.format(
            self.thing, self.value, self.article_id)


class Signal(db.Model):
    __tablename__ = 'signals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    plase_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, nullable=False)
    things = db.relationship('SignalThing', backref='thing', lazy='dynamic')

    def __init__(self, type, user_created_id, plase_id):
        self.type = type
        self.user_created_id = user_created_id
        self.plase_id = plase_id
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return '<Signal (id={})>'.format(self.id)


class SignalThing(db.Model):
    __tablename__ = 'signal_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thing = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    signal_id = db.Column(db.Integer, db.ForeignKey('signals.id'))

    def __init__(self, thing, value, signal_id):
        self.thing = thing
        self.value = value
        self.signal_id = signal_id

    def __repr__(self):
        return '<SignalThing (thing={}, value={}, signal_id={})>'.format(
            self.thing, self.value, self.article_id)


if __name__ == '__main__':
    manager.run()
