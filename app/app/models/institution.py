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
    institution_type_id = Column(Integer, ForeignKey(
        "institution_type.id"), nullable=False)
    institution_type = relationship(
        "InstitutionType", back_populates="institutions")
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=True)
    admin = relationship("Admin", back_populates="institution", uselist=False)


class InstitutionType(Base):
    __tablename__ = 'institution_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    institutions = relationship(
        'Institution', back_populates="institution_type")
