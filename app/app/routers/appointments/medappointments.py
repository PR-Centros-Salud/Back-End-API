from fastapi import APIRouter, Depends, HTTPException, status
from config.database import get_db
from config.oauth2 import get_current_active_user
from schemas.appointments import MedicalAppointmentCreate
from sqlalchemy.orm import Session
from schemas.person.person import PersonGet
from cruds import appointments as crud_appointments

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