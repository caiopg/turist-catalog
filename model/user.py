from sqlalchemy import Column, Integer, String

from model.base import Base


class User(Base):
    """
    This class represents a user. A user has an ID, a  name and an e-mail
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
