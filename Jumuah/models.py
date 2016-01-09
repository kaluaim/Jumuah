from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    votes = db.relationship('Vote', backref='user', lazy='dynamic')

    def __init__(self, name, password, email, date_joined, last_login, admin=False):
        self.name = name
        self.password = password
        self.email = email
        self.date_joined = date_joined
        self.last_login = last_login
        self.admin = admin

    def __repr__(self):
        return '<User (name={}, password={}, email={})>'.format(self.name,
            self.password, self.email)


class Mosque(db.Model):
    __tablename__ = 'mosques'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    imam_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime, nullable=False)
    topics = db.relationship('Topic', backref='mosque', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Mosque (name={})>'.format(self.name)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String, nullable=False)
    province = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    district = db.Column(db.String, nullable=False)

    def __init__(self, country, province, city, district):
        self.country = country
        self.province = province
        self.city = city
        self.district = district

    def __repr__(self):
        return '<Location (country={}, province={}, city={},\
            district={})>'.format(self.country, self.province, self.city,
            self.district)


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

    def __init__(self, title):
        self.title = title

    def __init__(self):
        return '<Topic (title={})>'.format(self.title)
