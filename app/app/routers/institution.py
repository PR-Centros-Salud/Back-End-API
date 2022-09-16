from fastapi import APIRouter, Depends
from cruds import institution as crud_institution
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.institution import InstitutionCreate, InstitutionGet, InstitutionUpdate
from config.oauth2 import get_current_super_admin
from schemas.person.superadmin import SuperAdminGet

router = APIRouter(
    prefix="/institution",
    tags=["Institutions"]
)


@router.post("/create", response_model=InstitutionGet)
async def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_institution.create_institution(db=db, institution=institution)
