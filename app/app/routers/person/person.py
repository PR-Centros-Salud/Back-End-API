from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from cruds.person import person as crud_person, medicalPersonal as crud_medical
from schemas.person.person import PersonCreate, PersonGet, PersonUpdatePassword
from config.database import get_db
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from sqlalchemy import and_
from schemas.config.auth import Token, TokenData
import os
from models.appointments import MedicalAppointment, LaboratoryAppointment

router = APIRouter(
    prefix="/person",
    tags=["Persons"]
)

@router.get("/me")
async def read_users_me(db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user:
        current_user = current_user.__dict__
        if current_user['discriminator'] == 'medical_personal':
            current_user['contracts'] = crud_medical.get_contracts(db, current_user['id'])
            current_user['specializations'] = crud_medical.get_specializations(db, current_user['id'])
            db_appointment = db.query(MedicalAppointment).filter(
                and_(
                    MedicalAppointment.medical_personal_id == current_user['id'],
                    MedicalAppointment.status == 1,
                    MedicalAppointment.programmed_date == date.today()
                )
            ).all()

            if db_appointment:
                for ap in db_appointment:
                    ap.status = 3
                    db.commit()
                    db.refresh(ap)

            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(
                    MedicalAppointment.medical_personal_id == current_user['id'],
                    LaboratoryAppointment.status == 1,
                    LaboratoryAppointment.programmed_date == date.today(),
                )
            ).all()

            if db_appointment:
                for ap in db_appointment:
                    ap.status = 3
                    db.commit()
                    db.refresh(ap)
        if current_user['discriminator'] == 'client':
            db_appointment = db.query(MedicalAppointment).filter(
                and_(
                    MedicalAppointment.patient_id == current_user['id'],
                    MedicalAppointment.status == 1,
                    MedicalAppointment.programmed_date == date.today()
                )
            ).all()

            if db_appointment:
                for ap in db_appointment:
                    ap.status = 3
                    db.commit()
                    db.refresh(ap)

            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(
                    MedicalAppointment.patient_id == current_user['id'],
                    LaboratoryAppointment.status == 1,
                    LaboratoryAppointment.programmed_date == date.today(),
                )
            ).all()

            if db_appointment:
                for ap in db_appointment:
                    ap.status = 3
                    db.commit()
                    db.refresh(ap)

        del current_user['_password']
        return current_user
    else:
        raise HTTPException(status_code=400, detail="User not found")


@router.post("/login", response_model=Token)
async def login(
    # Change to user model
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": user.username, "discriminator": user.discriminator, "id": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.patch("/update-password")
async def update_password(
    person: PersonUpdatePassword,
    db: Session = Depends(get_db),
    current_user: PersonGet = Depends(get_current_active_user)
):
    return crud_person.update_password(db=db, person=person, id=current_user.id)
