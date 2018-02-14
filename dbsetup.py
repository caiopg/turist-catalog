from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

''' dbsetup is used to prepare the database. All of the necessary config
classes and methods can be found here and should be kept here.
'''

DB_PATH = 'sqlite:///touristcatalog.db'

Base = declarative_base()

'''This class represents a user. A user has an ID, a name and an e-mail.'''


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


'''This class represents a country. A country has an ID, a name,
a description and a user who created it in the database.'''


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


'''This class represents an attraction. An attraction has an ID, a name,
a city, a descripton, a country where it is located and a user who created
it in the database.'''


class Attraction(Base):
    __tablename__ = 'attraction'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    description = Column(String(250))
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'description': self.description,
            'country': self.country_id
        }


engine = create_engine(DB_PATH)

Base.metadata.create_all(engine)
