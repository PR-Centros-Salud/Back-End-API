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
# def get_appointment_by_id(db: Session, id: int):
#     return db.query(Appointment).filter(
#         and_(Appointment.id == id, Appointment.status == 1)).first()

def create_medical_appointment(db: Session, appointment: MedicalAppointmentCreate):
    try:
        institution = validate_institution(db, appointment.institution_id)
        contract = validate_contract(db, appointment.medical_personal_id, appointment.institution_id)
        appointment = validate_appointment(db, appointment, contract.schedule_id)

        # db_appointment = Appointment(**appointment.dict())
        # db.add(db_appointment)
        # db.commit()
        # db.refresh(db_appointment)
        # return db_appointment
        return appointment
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")
