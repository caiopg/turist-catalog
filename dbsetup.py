from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DB_PATH = 'sqlite:///touristcatalog.db'

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


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
