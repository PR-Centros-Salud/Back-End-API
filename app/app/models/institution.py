# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
# from models.person.medicalPersonal import MedicalInstitution


class Institution(BaseTable):
    __tablename__ = "institution"

    # Entity Fields
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    photo_url = Column(String(150), nullable=True)
    institution_type = Column(SmallInteger, nullable=False)

    # Relationships
    admin_id = Column(Integer, ForeignKey("admin.id"))
    admin = relationship("Admin", back_populates="institution")
    # medical_personal = relationship(
    #     "MedicalInstution", back_populates="institution")
