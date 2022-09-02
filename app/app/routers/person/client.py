import os
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from cruds.person import client as crud_client
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.person.client import ClientCreate, ClientGet, ClientUpdate, ClientUpdatePassword
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token

router = APIRouter(
    prefix="/client",
    tags=["Clients"]
)
# {
#   "discriminator": "client",
#   "updated_at": "2022-09-02T00:17:26",
#   "first_name": "Santiago",
#   "second_last_name": "Sainz",
#   "email": "sarabia@example.com",
#   "phone": "string",
#   "gender": "s",
#   "photo_url": null,
#   "id": 1,
#   "_password": "$2b$12$db2eVBQLG8ZYdWnTkpYZw.7qIF1JP1Ar.bj4LwrUtUdCeRYzh0x1y",
#   "created_at": "2022-09-02T00:17:26",
#   "status": 1,
#   "last_name": "Sarabia",
#   "username": "sarabia",
#   "identity_card": "string",
#   "address": "string",
#   "birthdate": "2022-09-01",
#   "province_id": 1
# }


@router.post("/create", response_model=ClientGet)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return crud_client.create_client(db=db, client=client)


@router.patch("/update", response_model=ClientGet)
async def update_client(client: ClientUpdate, db: Session = Depends(get_db), current_user: ClientGet = Depends(get_current_active_user)):
    return crud_client.update_client(db=db, client=client, id=current_user.id)


@router.patch("/update-password", response_model=ClientGet)
async def update_client_password(client: ClientUpdatePassword, db: Session = Depends(get_db), current_user: ClientGet = Depends(get_current_active_user)):
    return crud_client.update_client_password(db=db, client=client, id=current_user.id)


@router.delete("/delete")
async def delete_client(db: Session = Depends(get_db), current_user: ClientGet = Depends(get_current_active_user)):
    return crud_client.delete_client(db=db, id=current_user.id)
