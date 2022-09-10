# Library Importation
from models.baseTable import BaseTable

# Configs
from passlib.hash import bcrypt
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from models.location import Province


class Person(BaseTable):
    __tablename__ = "person"
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    second_last_name = Column(String(50), nullable=True)
    username = Column(String(30), nullable=False)
    email = Column(EmailType, nullable=False)
    _password = Column("password", String(200), nullable=False)
    identity_card = Column(String(30), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    birthdate = Column(Date, nullable=False)
    photo_url = Column(String(150), nullable=True)

    # Relationships
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)

    # province = relationship("Province", back_populates="person")
    discriminator = Column("role", String(50), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": discriminator
    }

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self._password)
