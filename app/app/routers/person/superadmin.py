from fastapi import FastAPI, HTTPException, APIRouter, Depends
from cruds.person import superadmin as crud_superadmin
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.person.superadmin import SuperAdminCreate, SuperAdminGet, SuperAdminUpdate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token

router = APIRouter(
    prefix="/superadmin",
    tags=["SuperAdmins"]
)


@router.post("/create", response_model=SuperAdminGet)
async def create_superadmin(superadmin: SuperAdminCreate, db: Session = Depends(get_db)):
    return crud_superadmin.create_superadmin(db=db, superadmin=superadmin)


@router.patch("/update", response_model=SuperAdminGet)
async def update_superadmin(superadmin: SuperAdminUpdate, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_active_user)):
    return crud_superadmin.update_superadmin(db=db, superadmin=superadmin, id=current_user.id)


@router.delete("/delete")
async def delete_superadmin(db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_active_user)):
    return crud_superadmin.delete_superadmin(db=db, id=current_user.id)
