from model import DBSession
from model.attraction import Attraction
from model.country import Country
from model.user import User

"""
dbhelper is used to interface with the database. All interaction
with the database should be done through it.
"""


class DbHelper:

    def __init__(self):
        self.session = DBSession()

    # Method retrieves all countries from database.
    def get_countries(self):
        return self.session.query(Country)

    # Method retrieves a specific country by its ID.
    def get_country_by_id(self, country_id):
        return self.session.query(Country).filter_by(id=country_id).first()

    # Method retrieves all attractions associated to a specific country.
    def get_attractions(self, country_id):
        return self.session.query(Attraction).filter_by(
            country_id=country_id).all()

    # Method retrieves a specific attractions by its ID.
    def get_attraction_by_id(self, attraction_id):
        return self.session.query(Attraction).filter_by(id=attraction_id) \
            .first()

    # Method adds entry to the database.
    def add_to_db(self, element):
        self.session.add(element)
        self.session.commit()

    # Method removes an entry from the database,
    def delete_from_database(self, element):
        self.session.delete(element)
        self.session.commit()

    # Method removes all attractions associated to a specific country.
    def delete_attractions_by_country_id(self, country_id):
        self.session.query(Attraction).filter_by(
            country_id=country_id).delete()
        self.session.commit()

    # Method retrieves a specific user by its e-mail.
    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()
