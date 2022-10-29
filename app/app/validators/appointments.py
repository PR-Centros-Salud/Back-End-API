from sqlalchemy.orm import Session
from app.app.models.person.medicalPersonal import MedicalPersonal
from models.appointments import Appointment
from models.institution import Institution
from schemas.appointments import AppointmentCreate, AppointmentGet, AppointmentUpdate
from validators.location import validate_location
from fastapi import HTTPException, status
from sqlalchemy import exc, and_
from validators.person.medicalPersonal import validate_medical_personal
from schemas.appointments import AppointmentCreate

def validate_appointment(db: Session, appointment_create: AppointmentCreate ) -> bool:
    db_medicalPersonal = validate_medical_personal(db, appointment_create.institution_id)

    if db_medicalPersonal.institution_type in [1,4]:
        if db.query(MedicalPersonal).filter(
            and_()).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Laboratory Service already exists"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution is not valid for this operation."
        )

    return True

##  VALDAR QUE EL DOCTOR TRBAJA, LA FEHA, Y QUE NO ESTE OCUPADO

