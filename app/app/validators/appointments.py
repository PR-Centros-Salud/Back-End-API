from sqlalchemy.orm import Session
from models.person.medicalPersonal import MedicalPersonal
from models.appointments import Appointment
from models.person.medicalPersonal import ScheduleDay, Schedule, ScheduleDayAppointment
from models.institution import Institution
from schemas.appointments import AppointmentCreate, AppointmentGet, AppointmentUpdate
from validators.location import validate_location
from fastapi import HTTPException, status
from sqlalchemy import exc, and_, or_
from validators.person.medicalPersonal import validate_medical_personal
from schemas.appointments import MedicalAppointmentCreate, LaboratoryAppointmentCreate
from datetime import timedelta, datetime
from typing import Union

def validate_appointment(
    db: Session,
    appointment_create: Union[MedicalAppointmentCreate, LaboratoryAppointmentCreate],
    schedule_id: int,
    schedule_day: ScheduleDay,
) -> bool:
    if appointment_create.programmed_date < (datetime.now().date() + timedelta(days=1)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Programmed date must be greater or equal to tomorrow",
        )
    db_schedule = (
        db.query(Schedule)
        .filter(and_(Schedule.id == schedule_id, Schedule.status == 1))
        .first()
    )

    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found"
        )

    db_schedule_day_appointment = (
        db.query(ScheduleDayAppointment)
        .filter(
            and_(
                ScheduleDayAppointment.schedule_day_id == schedule_day.id,
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
                Appointment.patient_id == appointment_create.patient_id,
                or_(Appointment.status == 1, Appointment.status == 2),
                Appointment.medical_personal_id
                == appointment_create.medical_personal_id,
            )
        )
        .first()
    )

    if db_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client already has a pending appointment with this medical personal",
        )

    db_appointment = (
        db.query(Appointment)
        .filter(
            and_(
                Appointment.patient_id == appointment_create.patient_id,
                or_(Appointment.status == 1, Appointment.status == 2),
                Appointment.programmed_date == appointment_create.programmed_date,
            )
        )
        .all()
    )

    if len(db_appointment) >= 0:
        db_schedule_day_appointment = (
            db.query(ScheduleDayAppointment)
            .filter(
                and_(
                    ScheduleDayAppointment.schedule_day_id == schedule_day.id,
                    ScheduleDayAppointment.status == 1,
                    ScheduleDayAppointment.id
                    == appointment_create.schedule_day_appointment_id,
                )
            )
            .first()
        )

        for appointment in db_appointment:
            db_schedule_day_appointment_2 = (
                db.query(ScheduleDayAppointment)
                .filter(
                    and_(
                        ScheduleDayAppointment.schedule_day_id == schedule_day.id,
                        ScheduleDayAppointment.status == 1,
                    )
                )
                .first()
            )

            if (
                db_schedule_day_appointment.start_time
                >= db_schedule_day_appointment_2.start_time
                and db_schedule_day_appointment.start_time
                <= db_schedule_day_appointment_2.end_time
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Client has an overlapping appointment",
                )

            if (
                db_schedule_day_appointment.end_time
                >= db_schedule_day_appointment_2.start_time
                and db_schedule_day_appointment.end_time
                <= db_schedule_day_appointment_2.end_time
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Client has an overlapping appointment",
                )

    db_appointment = (
        db.query(Appointment)
        .filter(
            and_(
                Appointment.schedule_day_appointment_id
                == db_schedule_day_appointment.id,
                or_(Appointment.status == 1, Appointment.status == 2),
                Appointment.programmed_date == appointment_create.programmed_date,
            )
        )
        .first()
    )

    if db_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment time has already been taken",
        )

    return True
