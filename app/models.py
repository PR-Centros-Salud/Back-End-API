from passlib.hash import bcrypt
from email.policy import default
from config.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, ForeignKey, Float, Boolean, create_engine
from sqlalchemy_utils import EmailType


class BaseTable(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    status = Column(SmallInteger, default=True)


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


class Experience(BaseTable):
    __tablename__ = 'experiences'

    # Entity Fields
    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False)
    company = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(500), nullable=False)


# class Country(Base):
#     __tablename__ = 'countries'

#     # Entity Fields
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)

#     # Audit Fields
#     user_id = Column(Integer, nullable=False, default=1)
#     created_at = Column(DateTime, nullable=False,
#                         default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, nullable=False,
#                         default=datetime.datetime.utcnow)
