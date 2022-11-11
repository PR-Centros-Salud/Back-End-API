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
    Time,
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
    is_lab_personal = Column(SmallInteger, nullable=False, default=0)

    medical_personal_id = Column(
        Integer, ForeignKey("medical_personal.id"), nullable=False
    )
    medical_personal = relationship("MedicalPersonal", back_populates="contract")

    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False)
    institution = relationship("Institution", back_populates="contract")

    schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=True)
    schedule = relationship("Schedule", back_populates="contract")


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
    contract = relationship("Contract", back_populates="medical_personal")
    specialization = relationship("Specialization", back_populates="medical_personal")
    appointment = relationship("Appointment", back_populates="medical_personal")
    laboratory_service = relationship(
        "LaboratoryService", back_populates="medical_personal"
    )
    

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


class Schedule(BaseTable):
    __tablename__ = "schedule"

    estimated_appointment_time = Column(Integer, nullable=False)

    # Relationships
    schedule_day = relationship("ScheduleDay", back_populates="schedule")
    contract = relationship("Contract", back_populates="schedule", uselist=False)


class ScheduleDay(BaseTable):
    __tablename__ = "schedule_day"

    day = Column(SmallInteger, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relationships
    schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="schedule_day")

    room_id = Column(Integer, ForeignKey("room.id"), nullable=True)
    room = relationship("Room", back_populates="schedule_day")

    schedule_day_appointment = relationship(
        "ScheduleDayAppointment", back_populates="schedule_day"
    )


class ScheduleDayAppointment(BaseTable):
    __tablename__ = "schedule_day_appointment"

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relationships
    schedule_day_id = Column(Integer, ForeignKey("schedule_day.id"), nullable=False)
    schedule_day = relationship(
        "ScheduleDay", back_populates="schedule_day_appointment"
    )

    appointment = relationship("Appointment", back_populates="schedule_day_appointment")
