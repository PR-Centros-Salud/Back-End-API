# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Institution(BaseTable):
    __tablename__ = 'institution'

    # Entity Fields
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)

    # Relationships
    institution_type_id = Column(Integer, ForeignKey(
        "institution_type.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("admin.id"))
    admin = relationship("Admin", back_populates="institution")
    medical_personal = relationship(
        "MedicalInstution", back_populates="institution")


class InstitutionType(BaseTable):
    __tablename__ = "institution_type"

    name = Column(String(100), nullable=False)

    # Relationships
    institution = relationship("Institution")
