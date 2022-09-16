import os
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from cruds.person import client as crud_client
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.person.client import ClientCreate, ClientGet, ClientUpdate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token

router = APIRouter(
    prefix="/client",
    tags=["Clients"]
)


@router.post("/create", response_model=ClientGet)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return crud_client.create_client(db=db, client=client)


@router.patch("/update", response_model=ClientGet)
async def update_client(client: ClientUpdate, db: Session = Depends(get_db), current_user: ClientGet = Depends(get_current_active_user)):
    return crud_client.update_client(db=db, client=client, id=current_user.id)


@router.delete("/delete")
async def delete_client(db: Session = Depends(get_db), current_user: ClientGet = Depends(get_current_active_user)):
    return crud_client.delete_client(db=db, id=current_user.id)
