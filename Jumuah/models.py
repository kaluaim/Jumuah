from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    date_joined = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User (name={}, password={}, email={})>'.format(self.name,
            self.password, self.email)


class Mosque(db.Model):
    __tablename__ = 'mosques'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    imam_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #date added

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Mosque (name={})>'.format(self.name)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)
    province = db.Column(db.String)
    city = db.Column(db.String)
    district = db.Column(db.String)

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
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #date of vote

    def __init__(self):
        pass

    def __repr__(self):
        return '<Vote (topic={})>'.format(self.topic_id)


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosques.id'))
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title):
        self.title = title

    def __init__(self):
        return '<Topic (title={})>'.format(self.title)
