from sqlalchemy.orm import Session
from models.person.medicalPersonal import MedicalPersonal
from models.appointments import Appointment
from models.person.medicalPersonal import ScheduleDay, Schedule, ScheduleDayAppointment
from models.institution import Institution
from schemas.appointments import AppointmentCreate, AppointmentGet, AppointmentUpdate
from validators.location import validate_location
from fastapi import HTTPException, status
from sqlalchemy import exc, and_
from validators.person.medicalPersonal import validate_medical_personal
from schemas.appointments import AppointmentCreate
from datetime import timedelta, datetime


def validate_appointment(
    db: Session, appointment_create: AppointmentCreate, schedule_id: int
) -> bool:
    day = appointment_create.programmed_date.weekday() + 1
    db_schedule = (
        db.query(Schedule)
        .filter(and_(Schedule.id == schedule_id, Schedule.status == 1))
        .first()
    )

    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found"
        )

    db_schedule_day = (
        db.query(ScheduleDay)
        .filter(
            and_(
                ScheduleDay.schedule_id == schedule_id,
                ScheduleDay.day == day,
                ScheduleDay.status == 1,
            )
        )
        .first()
    )

    if not db_schedule_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal does not work on this day",
        )

    db_schedule_day_appointment = (
        db.query(ScheduleDayAppointment)
        .filter(
            and_(
                ScheduleDayAppointment.schedule_day_id == db_schedule_day.id,
                ScheduleDayAppointment.status == 1,
                ScheduleDayAppointment.id
                == appointment_create.schedule_day_appointment_id,
            )
        )
        .first()
    )

    if not db_schedule_day_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal does not work on this time",
        )

    db_appointment = (
        db.query(Appointment)
        .filter(
            and_(
                Appointment.schedule_day_appointment_id
                == db_schedule_day_appointment.id,
                Appointment.status == 1,
                Appointment.programmed_date == appointment_create.programmed_date,
            )
        )
        .first()
    )

    if db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment already exists",
        )

    db_appointment = (
        db.query(Appointment)
        .filter(
            and_(
                Appointment.patient_id == appointment_create.client_id,
                or_(Appointment.status == 1, Appointment.status == 2),
                Appointment.medical_personal_id
                == appointment_create.medical_personal_id,
            )
        )
        .first()
    )

    if db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client already has an appointment",
        )

    return appointment_create
