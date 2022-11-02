from models.appointments import Appointment, MedicalAppointment, LaboratoryAppointment
from validators.institution import validate_institution
from models.location import Province
from schemas.appointments import AppointmentGet, AppointmentCreate, AppointmentUpdate, MedicalAppointmentFinished, MedicalAppointmentGet, LaboratoryAppointmentFinished
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.person.medicalPersonal import validate_contract
from validators.appointments import validate_appointment
from cruds.person.person import delete_person
from schemas.appointments import MedicalAppointmentCreate
from models.person.medicalPersonal import ScheduleDay
from schemas.person.person import PersonGet
from typing import Union
from datetime import date

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

def update_appointment(db: Session, id: int, status: int, user: PersonGet, appointment_type: int):
    try:
        db_appointment = None

        if appointment_type == 1:
            db_appointment = db.query(MedicalAppointment).filter(
                and_(MedicalAppointment.id == id, MedicalAppointment.status == 2)
            ).first()
        else:
            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(LaboratoryAppointment.id == id, LaboratoryAppointment.status == 2)
            ).first()

        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if status == 2 and user.id != db_appointment.medical_personal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have permission to confirm this appointment",
            )

        if status == 2 and db_appointment.status == 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been confirmed",
            )

        if status == 3 and db_appointment.status == 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been canceled",
            )


        if status == 3 and user.id != db_appointment.patient_id and user.id != db_appointment.medical_personal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have permission to cancel this appointment",
            )

        db_appointment.status = status
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def finish_appointment(db: Session, id: int, user: PersonGet, finished : Union[MedicalAppointmentFinished, LaboratoryAppointmentFinished]):
    try:
        db_appointment = None 

        if type(finished) == MedicalAppointmentFinished:
            db_appointment = db.query(MedicalAppointment).filter(
                and_(MedicalAppointment.id == id, MedicalAppointment.status == 2)
            ).first()
        else: 
            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(LaboratoryAppointment.id == id, LaboratoryAppointment.status == 2)
            ).first()

        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if user.id != db_appointment.medical_personal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have permission to finish this appointment",
            )
        
        if db_appointment.programmed_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't finish an appointment before the programmed date",
            )

        db_appointment.status = 4

        if type(finished) == MedicalAppointmentFinished:
            if (finished.recipe):
                db_appointment.recipe = finished.recipe
        else:
            db_appointment.delivery_datetime = finished.delivery_datetime

            if (finished.result):
                db_appointment.result = finished.result

        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def get_medical_personal_appointments(db: Session, medical_personal_id: int, status: int):
    try:
        db_appointments = (
            db.query(MedicalAppointment)
            .filter(
                and_(
                    MedicalAppointment.medical_personal_id == medical_personal_id,
                    MedicalAppointment.status == status,
                )
            )
            .all()
        )
        return db_appointments
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def get_patient_appointments(db: Session, patient_id: int, status: int):
    try:
        db_appointments = (
            db.query(MedicalAppointment)
            .filter(
                and_(
                    MedicalAppointment.patient_id == patient_id,
                    MedicalAppointment.status == status,
                )
            )
            .all()
        )
        return db_appointments
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )