from models.appointments import Appointment, MedicalAppointment
from validators.institution import validate_institution
from models.location import Province
from schemas.appointments import AppointmentGet, AppointmentCreate, AppointmentUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.person.medicalPersonal import validate_contract
from validators.appointments import validate_appointment
from cruds.person.person import delete_person
from schemas.appointments import MedicalAppointmentCreate
from models.person.medicalPersonal import ScheduleDay

# def get_appointment_by_id(db: Session, id: int):
#     return db.query(Appointment).filter(
#         and_(Appointment.id == id, Appointment.status == 1)).first()


def create_medical_appointment(db: Session, appointment: MedicalAppointmentCreate):
    try:
        institution = validate_institution(db, appointment.institution_id)
        contract = validate_contract(
            db, appointment.medical_personal_id, appointment.institution_id
        )
        day = appointment.programmed_date.weekday() + 1
        db_schedule_day = (
            db.query(ScheduleDay)
            .filter(
                and_(
                    ScheduleDay.schedule_id == contract.schedule_id,
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

        if validate_appointment(db, appointment, contract.schedule_id, db_schedule_day):
            db_appointment = MedicalAppointment(
                patient_id=appointment.patient_id,
                medical_personal_id=appointment.medical_personal_id,
                institution_id=appointment.institution_id,
                schedule_day_appointment_id=appointment.schedule_day_appointment_id,
                programmed_date=appointment.programmed_date,
                room_id=db_schedule_day.room_id,
            )
            db.add(db_appointment)
            db.commit()
            db.refresh(db_appointment)
            return db_appointment

    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )
