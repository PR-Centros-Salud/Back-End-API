from passlib.hash import bcrypt
from email.policy import default
from config.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, ForeignKey, Float, Boolean, create_engine
from sqlalchemy_utils import EmailType


class Person(BaseTable):
    __tablename__ = "person"
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    second_last_name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(EmailType, nullable=False, unique=True)
    _password = Column("password", String(200), nullable=False)
    identity_card = Column(String(30), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    birthdate = Column(DateTime, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self._password)
