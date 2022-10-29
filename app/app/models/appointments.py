from models.baseTable import BaseTable
from sqlalchemy import (
    Date,
    Time,
    SmallInteger,
    Integer,
    DateTime,
    Column,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime


class Appointment(BaseTable):
    __tablename__ = "appointment"
    programmed_date = Column(Date, nullable=False)
    # Relationships
    medical_personal_id = Column(
        Integer, ForeignKey("medical_personal.id"), nullable=False
    )
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False)
    medical_personal = relationship("MedicalPersonal", back_populates="appointment")
    client = relationship("Client", back_populates="appointment")
    room = relationship("Room", back_populates="appointment")
    institution = relationship("Institution", back_populates="appointment")
    discriminator = Column("type", String(50), nullable=False)
    schedule_day_appointment_id = Column(
        Integer, ForeignKey("schedule_day_appointment.id"), nullable=False
    )
    schedule_day_appointment = relationship(
        "ScheduleDayAppointment", back_populates="appointment"
    )

    __mapper_args__ = {
        "polymorphic_identity": "appointment",
        "polymorphic_on": discriminator,
    }


class MedicalAppointment(Appointment):
    __tablename__ = "medical_appointment"
    __mapper_args__ = {"polymorphic_identity": "medical_appointment"}
    id = Column(Integer, ForeignKey("appointment.id"), primary_key=True)
    medical_appointment_created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    medical_appointment_updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow
    )
    medical_appointment_status = Column(SmallInteger, default=1, nullable=False)
    medical_appointment_recipe = Column(String(500), nullable=True)


class LaboratoryAppointment(Appointment):
    __tablename__ = "laboratory_appointment"
    __mapper_args__ = {"polymorphic_identity": "laboratory_appointment"}
    id = Column(Integer, ForeignKey("appointment.id"), primary_key=True)
    laboratory_appointment_created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    laboratory_appointment_updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow
    )
    laboratory_appointment_status = Column(SmallInteger, default=1, nullable=False)
    laboratory_delivery_date = Column(DateTime, nullable=True)
    laboratory_results_resume = Column(String(500), nullable=True)
    laboratory_service_id = Column(
        Integer, ForeignKey("laboratory_service.id"), nullable=False
    )
    laboratory_service = relationship(
        "LaboratoryService", back_populates="laboratory_appointment"
    )
