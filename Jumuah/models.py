from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name,
        self.fullname, self.password)


class Mosuq(Base):
    __tablename__ = 'mosuqes'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Location(Base):
    __tablename__ = 'locations'


class Vote(Base):
    __tablename__ = 'votes'


class Topic(Base):
    __tablename__ = 'topics'
