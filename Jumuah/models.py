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


class Mosque(Base):
    __tablename__ = 'mosques'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location_id = (Integer, ForeignKey('location.id'))
    imam_id = (Integer, ForeignKey('user.id'))



class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)


class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
