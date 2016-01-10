import datetime
from flask.ext.login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    votes = db.relationship('Vote', backref='user', lazy='dynamic')

    def __init__(self, password, email, name='', admin=False):
        self.name = name
        self.password = password
        self.email = email
        self.date_joined = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '<User (name={}, password={}, email={})>'.format(self.name,
            self.password, self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Mosque(db.Model):
    __tablename__ = 'mosques'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    province = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    district = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    topics = db.relationship('Topic', backref='mosque', lazy='dynamic')

    def __init__(self, name, country, province, city, district):
        self.name = name
        self.country = country
        self.province = province
        self.city = city
        self.district = district
        self.date_added = datetime.datetime.now()

    def __repr__(self):
        return '<Mosque (name={})>'.format(self.name)


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vote_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, vote_date):
        self.vote_date = vote_date

    def __repr__(self):
        return '<Vote (topic={})>'.format(self.topic_id)


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosques.id'))
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    votes = db.relationship('Vote', backref='topic', lazy='dynamic')

    def __init__(self, title, user_created_id, mosque_id):
        self.title = title
        self.user_created_id=user_created_id
        self.mosque_id = mosque_id

    def __repr__(self):
        return '<Topic (title={})>'.format(self.title)
