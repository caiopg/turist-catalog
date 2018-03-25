from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from model.base import Base
from model.country import Country
from model.user import User


class Attraction(Base):
    """
    This class represents an attraction. An attraction has an ID, a name,
    a city, a description, a country where it is located and a user who
    created it in the database.
    """

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
