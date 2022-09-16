from fastapi import FastAPI, HTTPException, APIRouter, Depends
from cruds.person import admin as crud_admin
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.person.admin import AdminCreate, AdminGet, AdminUpdate
from schemas.person.superadmin import SuperAdminGet
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token, get_current_super_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admins"]
)


@router.post("/create", response_model=AdminGet,)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_admin.create_admin(db=db, admin=admin)


@router.patch("/update", response_model=AdminGet)
async def update_admin(admin: AdminUpdate, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_active_user)):
    return crud_admin.update_admin(db=db, admin=admin, id=current_user.id)


@router.delete("/delete/{admin_id}")
async def delete_admin(admin_id: int, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_admin.delete_admin(db=db, id=admin_id)
