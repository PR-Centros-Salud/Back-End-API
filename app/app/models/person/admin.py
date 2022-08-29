# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Admin(Person):
    __tablename__ = 'admin'
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    # Entity Fields
    id = Column(Integer, primary_key=True)
    institution_id = Column(Integer, ForeignKey(
        'institution.id'), nullable=True)
    institution = relationship(
        "Institution", back_populates="admins", uselist=False)
