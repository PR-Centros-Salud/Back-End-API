from fastapi import APIRouter, Depends, HTTPException, status
from config.database import get_db
from config.oauth2 import get_current_active_user
from schemas.appointments import MedicalAppointmentCreate, MedicalAppointmentFinished
from sqlalchemy.orm import Session
from schemas.person.person import PersonGet
from cruds import appointments as crud_appointments
from datetime import date

router = APIRouter(
    prefix="/medappointments",
    tags=["MedAppointments"]
)

@router.post("/create")
async def create_appointment(appointment: MedicalAppointmentCreate, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "client":
        appointment.patient_id = current_user.id
        return crud_appointments.create_medical_appointment(db=db, appointment=appointment)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.get('/get/{id}')
async def get_appointments(id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    return crud_appointments.get_appointment(db, user=current_user.id, id=id, type=0)

@router.patch('/confirm/{id}')
async def confirm_appointment(id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal":
        return crud_appointments.update_appointment(db=db, id=id, appointment_status=2, user=current_user, appointment_type=1)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a medical personal")

@router.patch('/cancel/{id}')
async def cancel_appointment(id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal" or current_user.discriminator == "client":
        return crud_appointments.update_appointment(db=db, id=id, appointment_status=3, user=current_user, appointment_type=1)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a medical personal")

@router.patch('/finish/{id}')
async def update_appointment(appointment: MedicalAppointmentFinished, id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal":
        return crud_appointments.finish_appointment(db=db, id=id, user=current_user, finished=appointment)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a medical personal")

@router.get('/medical_personal')
async def get_medical_personal_appointments(q: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal":
        return crud_appointments.get_medical_personal_appointments(db=db, medical_personal_id=current_user.id, appointment_status=q, type=1)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a medical personal")

@router.get('/client')
async def get_client_appointments(q: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "client":
        return crud_appointments.get_client_appointments(db=db, patient_id=current_user.id, q=q, type=1)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.get('/available-times/{id}')
async def get_available_times(id: int, date_time: date, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    return crud_appointments.get_available_times(db=db, doctor_id=id, date_time=date_time)

    