# Library Importation
from models.person.person import Person

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Date,
    SmallInteger,
    DateTime,
)
from sqlalchemy.orm import relationship
from models.baseTable import BaseTable


class Contract(BaseTable):
    __tablename__ = "contract"

    # Relationships
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)
    department = Column(String(50), nullable=True)
    role = Column(String(100), nullable=False)

    medical_personal_id = Column(
        Integer, ForeignKey("medical_personal.id"), nullable=False
    )
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False)

    institution = relationship("Institution", back_populates="contract")
    medical_personal = relationship(
        "MedicalPersonal", back_populates="contract"
    )


class MedicalPersonal(Person):
    __tablename__ = "medical_personal"
    __mapper_args__ = {"polymorphic_identity": "medical_personal"}

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    medical_personal_created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    medical_personal_updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow
    )
    medical_personal_status = Column(SmallInteger, default=1, nullable=False)

    # Relationships
    contract = relationship(
        "Contract", back_populates="medical_personal"
    )
    specialization = relationship("Specialization", back_populates="medical_personal")


class Specialization(BaseTable):
    __tablename__ = "specialization"
    specialization_name = Column(String(100), nullable=False)
    degree = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    location = Column(String(50), nullable=False)
    institution = Column(String(50), nullable=False)
    degree_photo_url = Column(String(100), nullable=True)

    # Relationships
    medical_personal_id = Column(Integer, ForeignKey("medical_personal.id"))
    medical_personal = relationship("MedicalPersonal", back_populates="specialization")
