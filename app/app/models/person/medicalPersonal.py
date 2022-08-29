# Library Importation
from models.person.person import Person
from models.institution import Institution

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date


medical_institution = Table(
    "medical_institution",
    Base.metadata,
    Column("person_id", Integer, ForeignKey("person.id")),
    Column("institution_id", Integer, ForeignKey("institution.id")),
    Column("start_date", Date, nullable=False),
    Column("end_date", Date, nullable=True),
    Column("role", String(50))
)


class MedicalPersonal(Person):
    __tablename__ = "medical_personal"
    __mapper_args__ = {"polymorphic_identity": "medical_personal"}

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    institution = relationship(
        "Institution", back_populates="admins", uselist=False)


class Experience(BaseTable):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False)
    company = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    person = relationship("Person", back_populates="experiences")
