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


@router.get("/", response_model=list[InstitutionGet])
def get_all_institutions(db: Session = Depends(get_db)):
    return crud_institution.get_all_institutions(db)

@router.post("/create", response_model=InstitutionGet)
async def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_institution.create_institution(db=db, institution=institution)


@router.patch("/update/{id}", response_model=InstitutionGet)
async def update_institution(institution: InstitutionUpdate, id: int, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_institution.update_institution(db=db, institution=institution, id=id)


@router.delete("/delete/{id}", response_model=InstitutionGet)
async def delete_institution(id: int, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_institution.delete_institution(db=db, id=id)
