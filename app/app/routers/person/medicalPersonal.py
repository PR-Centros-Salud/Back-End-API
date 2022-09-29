from fastapi import APIRouter, Depends
from cruds.person import medicalPersonal as crud_medicalPersonal
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.person.medicalPersonal import MedicalPersonalCreate, MedicalPersonalGet, MedicalPersonalUpdate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token

router = APIRouter(
    prefix="/medicalPersonal",
    tags=["MedicalPersonal"]
)


@router.post("/create", response_model=MedicalPersonalGet)
async def create_medical_personal(medicalPersonal: MedicalPersonalCreate, db: Session = Depends(get_db)):
    return crud_medicalPersonal.create_MedicalPersonal(db, medicalPersonal)(db=db, medicalPersonal=medicalPersonal)


@router.patch("/update", response_model=MedicalPersonalGet)
async def update_medical_personal(medicalPersonal: MedicalPersonalUpdate, db: Session = Depends(get_db), current_user: MedicalPersonalGet = Depends(get_current_active_user)):
    return crud_medicalPersonal.update_MedicalPersonal(db, medicalPersonal, id)(db=db, medicalPersonal=medicalPersonal, id=current_user.id)


@router.delete("/delete")
async def delete_medical_personal(db: Session = Depends(get_db), current_user: MedicalPersonalGet = Depends(get_current_active_user)):
    return crud_medicalPersonal.delete_medicalPersonal(db=db, id=current_user.id)