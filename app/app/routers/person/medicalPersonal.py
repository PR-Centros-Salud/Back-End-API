from fastapi import APIRouter, Depends
from cruds.person import medicalPersonal as crud_medicalPersonal
from typing import Union
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.person.medicalPersonal import MedicalPersonalCreate, MedicalPersonalGet, MedicalPersonalUpdate, SpecializationCreate, SpecializationUpdate, ContractCreate
from schemas.person.admin import AdminGet
from schemas.person.person import PersonGet
from validators.person.medicalPersonal import validate_medical_personal, validate_contract
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.oauth2 import get_current_active_user, authenticate_user, create_access_token, get_current_admin, get_current_medical
from fastapi import HTTPException, status
router = APIRouter(
    prefix="/medicalPersonal",
    tags=["MedicalPersonal"]
)


@router.post("/create", response_model=MedicalPersonalGet)
async def create_medical_personal(medicalPersonal: MedicalPersonalCreate, db: Session = Depends(get_db), current_user : AdminGet = Depends(get_current_admin)):
    return crud_medicalPersonal.create_MedicalPersonal(db, medicalPersonal)


@router.patch("/update", response_model=MedicalPersonalGet)
async def update_medical_personal(medicalPersonal: MedicalPersonalUpdate, db: Session = Depends(get_db), current_user: MedicalPersonalGet = Depends(get_current_medical)):
    return crud_medicalPersonal.update_MedicalPersonal(db, medicalPersonal, current_user.id)


@router.delete("/delete/{medical_id}")
async def delete_medical_personal(medical_id: int, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    if current_user.discriminator == "admin":
            return crud_medicalPersonal.remove_medicalPersonal(db, medical_id, current_user.institution_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You are not an admin"
        )

@router.post("/add-contract")
async def add_contract(contract: ContractCreate, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    if current_user.discriminator == "superadmin":
        contract = contract.dict()
        if validate_contract(db, contract["medical_personal_id"], contract["institution_id"]):
            return crud_medicalPersonal.create_medical_contract(db, contract)
        raise HTTPException(status_code=403, detail="You don't have permission to add contract")
    else:
        contract = contract.dict()
        contract["institution_id"] = current_user.institution_id
        if validate_contract(db, contract["medical_personal_id"], current_user.institution_id):
            return crud_medicalPersonal.create_medical_contract(db, contract)

@router.post("/add-specialization")
async def add_specialization(specialization: SpecializationCreate, db: Session = Depends(get_db), current_user: MedicalPersonalGet = Depends(get_current_medical)):
    return crud_medicalPersonal.add_specialization(db, specialization, current_user.id)

@router.patch("/update-specialization/{specialization_id}")
async def update_specialization(specialization_id : int, specialization: SpecializationUpdate, db: Session = Depends(get_db), current_user: MedicalPersonalGet = Depends(get_current_medical)):
    return crud_medicalPersonal.update_specialization(db, specialization_id, specialization, current_user.id)

@router.delete("/remove-specialization/{specialization_id}")
async def remove_specialization(specialization_id : int, db: Session = Depends(get_db), current_user: MedicalPersonalGet = Depends(get_current_medical)):
    return crud_medicalPersonal.delete_specialization(db, specialization_id, current_user.id)