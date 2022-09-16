# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger, Float
from sqlalchemy.orm import relationship
from schemas.institution import InstitutionType
# from models.person.medicalPersonal import MedicalInstitution


class Institution(BaseTable):
    __tablename__ = "institution"

    # Entity Fields
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    photo_url = Column(String(150), nullable=True)
    institution_type = Column(SmallInteger, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relationships
    admin = relationship("Admin", back_populates="institution")
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    # medical_personal = relationship(
    #     "MedicalInstution", back_populates="institution")
