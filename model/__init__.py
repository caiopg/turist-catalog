from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import base
from model.attraction import Attraction
from model.country import Country
from model.user import User

DB_PATH = 'sqlite:///touristcatalog.db'

engine = create_engine(DB_PATH)

base.Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
