from fastapi import APIRouter, Depends, HTTPException, status
from config.database import get_db
from config.oauth2 import get_current_active_user
from schemas.appointments import LaboratoryAppointmentCreate, LaboratoryAppointmentFinished
from sqlalchemy.orm import Session
from schemas.person.person import PersonGet
from cruds import appointments as crud_appointments
from models.laboratoryService import LaboratoryService

router = APIRouter(
    prefix="/labappointments",
    tags=["LabAppointments"]
)

@router.post("/create")
async def create_appointment(appointment: LaboratoryAppointmentCreate, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "client":
        laboratory_service = db.query(LaboratoryService).filter(LaboratoryService.id == appointment.laboratory_service_id).first()
        if laboratory_service is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laboratory service not found")
        
        appointment.medical_personal_id = laboratory_service.medical_personal_id
        appointment.institution_id = laboratory_service.institution_id
        appointment.patient_id = current_user.id

        return crud_appointments.create_medical_appointment(db=db, appointment=appointment)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.get('/get/{id}')
async def get_appointment(id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    return crud_appointments.get_appointment(db=db, user=current_user.id, id=id,type=1)

@router.patch('/confirm/{id}')
async def confirm_appointment(id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal":
        return crud_appointments.update_appointment(db=db, id=id, appointment_status=2, user=current_user, type=2)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.patch('/cancel/{id}')
async def cancel_appointment(id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal" or current_user.discriminator == "client":
        return crud_appointments.update_appointment(db=db, id=id, appointment_status=3, user=current_user, type=2)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.patch('/finish/{id}')
async def finish_appointment(id: int, appointment: LaboratoryAppointmentFinished, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal":
        return crud_appointments.finish_appointment(db, id=id, user=current_user, finished=appointment)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.get('/medical_personal')
async def get_medical_personal_appointments(q: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "medical_personal":
        return crud_appointments.get_medical_personal_appointments(db, medical_personal_id=current_user.id, appointment_status=q, type=2)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")

@router.get('/client')
async def get_client_appointments(q: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user.discriminator == "client":
        return crud_appointments.get_client_appointments(db, patient_id=current_user.id, q=q, type=2)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a client")