# Auth
# def verify_password()
from config.database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Auth
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.person.person import Person
from models.person.admin import Admin
from models.person.client import Client
from models.person.medicalPersonal import MedicalPersonal
from cruds.person.person import get_person_username, get_person_by_username
from schemas.config.auth import Token, TokenData

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password, person: Person):
    return person.verify_password(password)


def get_user(db, username: str):
    user = get_person_username(db, username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_person_username(db, username)
    if not user:
        return False
    if not verify_password(password, user):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        "SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"),
                             algorithms=[os.getenv("ALGORITHM")])

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    print(username)
    user = get_person_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.status != 1:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        if current_user.discriminator == "admin":
            user = db.query(Admin).filter(Admin.id == current_user.id).first()
        elif current_user.discriminator == "client":
            user = db.query(Client).filter(
                Client.id == current_user.id).first()
        else:
            user = db.query(MedicalPersonal).filter(
                MedicalPersonal.id == current_user.id).first()

        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password")

        return current_user
