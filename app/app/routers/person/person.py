import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from cruds.person.person import create_person
from schemas.person.person import PersonCreate, PersonGet
from config.database import get_db
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from schemas.config.auth import Token, TokenData
from models.person.admin import Admin
from models.person.client import Client
from models.person.medicalPersonal import MedicalPersonal

load_dotenv()

router = APIRouter(
    prefix="/person",
    tags=["Persons"]
)


@router.get("/me")
async def read_users_me(db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    if current_user:
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
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
