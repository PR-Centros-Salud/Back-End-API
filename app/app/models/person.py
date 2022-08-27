# Library Importation
from models.baseTable import BaseTable

# Configs
from passlib.hash import bcrypt
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy_utils import EmailType


class Person(BaseTable):
    __tablename__ = "person"
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(30), nullable=False)
    second_last_name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(EmailType, nullable=False, unique=True)
    _password = Column("password", String(200), nullable=False)
    identity_card = Column(String(30), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    birthdate = Column(Date, nullable=False)
    photo = Column(String(50), nullable=True)
    discriminator = Column("role", String(50), nullable=False)
    __mapper_args__ = {'polymorphic_on': discriminator}

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self._password)


# class
class Admin(Person):
    __tablename__ = "admin"
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)


class Client(Person):
    __tablename__ = "client"
    __mapper_args__ = {'polymorphic_identity': 'client'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)


class MedicalPersonal(Person):
    __tablename__ = "medical_personal"
    __mapper_args__ = {'polymorphic_identity': 'medical_personal'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
