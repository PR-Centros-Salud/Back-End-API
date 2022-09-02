# Library Importation
from models.person.person import Person

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, SmallInteger
from sqlalchemy.orm import relationship
from models.baseTable import BaseTable


# class MedicalInstitution(Base):
#     __tablename__ = "medical_institution"

#     # Relationships
#     medical_personal_id = Column(Integer, ForeignKey(
#         "medical_personal.id"), primary_key=True)
#     institution_id = Column(Integer, ForeignKey(
#         "institution.id"), primary_key=True)
#     start_date = Column(Date, nullable=False)
#     end_date = Column(Date, nullable=True)
#     department = Column(String(50), nullable=False)
#     role = Column(SmallInteger, nullable=False)

#     # Relationships
#     medical_personal = relationship(
#         "MedicalPersonal", back_populates="medical_institution")
#     institution_id = relationship(
#         "Institution", back_populates="medical_personal")


class MedicalPersonal(Person):
    __tablename__ = "medical_personal"
    __mapper_args__ = {"polymorphic_identity": "medical_personal"}

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)

    # Relationships
    # medical_institution = relationship(
    #     "MedicalInstitution", back_populates="medical_personal")
    experience = relationship(
        "Experience", back_populates="medical_personal")
    specialization = relationship(
        "Specialization", back_populates="medical_personal")


class Experience(BaseTable):
    __tablename__ = "experience"

    role = Column(String(50), nullable=False)
    company = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Relationships
    medical_personal_id = Column(Integer, ForeignKey("medical_personal.id"))
    medical_personal = relationship(
        "MedicalPersonal", back_populates="experience")


class Specialization(BaseTable):
    __tablename__ = "specialization"

    degree = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    location = Column(String(50), nullable=False)
    institution = Column(String(50), nullable=False)
    degree_photo_url = Column(String(100), nullable=False)
    finished = Column(SmallInteger, nullable=False)

    # Relationships
    medical_personal_id = Column(Integer, ForeignKey("medical_personal.id"))
    medical_personal = relationship(
        "MedicalPersonal", back_populates="specialization")
