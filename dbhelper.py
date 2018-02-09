from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import Base, DB_PATH, Country, Attraction, User


class DbHelper:

    def __init__(self):
        engine = create_engine(DB_PATH)
        Base.metadata.bind = engine

        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def get_countries(self):
        return self.session.query(Country)

    def get_country_by_id(self, country_id):
        return self.session.query(Country).filter_by(id=country_id).one()

    def get_attractions(self, country_id):
        return self.session.query(Attraction).filter_by(
            country_id=country_id).all()

    def get_attraction_by_id(self, attraction_id):
        return self.session.query(Attraction).filter_by(id=attraction_id).one()

    def add_to_db(self, element):
        self.session.add(element)
        self.session.commit()

    def delete_from_database(self, element):
        self.session.delete(element)
        self.session.commit()

    def delete_attractions_by_country_id(self, country_id):
        self.session.query(Attraction).filter_by(
            country_id=country_id).delete()
        self.session.commit()

    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).one()
