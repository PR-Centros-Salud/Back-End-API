from config.database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# import timedelta
from datetime import datetime, timedelta
import sys

# Auth
import os
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from routers.person import client, person, admin, superadmin, medicalPersonal
from routers import institution
from routers.appointments import medappointments, labappointments
from config.database import Base
from schemas.config.auth import Token, TokenData
from config.oauth2 import authenticate_user, create_access_token
from fastapi.middleware.cors import CORSMiddleware

sys.dont_write_bytecode = True

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(client.router)
app.include_router(person.router)
app.include_router(admin.router)
app.include_router(superadmin.router)
app.include_router(institution.router)
app.include_router(medicalPersonal.router)
app.include_router(medappointments.router)
app.include_router(labappointments.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/token", response_model=Token)
async def login(
    # Change to user model
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
