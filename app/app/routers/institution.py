from typing import Union
from fastapi import APIRouter, Depends
from cruds import institution as crud_institution
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.institution import InstitutionCreate, InstitutionGet, InstitutionUpdate, RoomCreate, RoomGet
from schemas.laboratoryService import LaboratoryServiceCreate, LaboratoryServiceGet, LaboratoryServiceUpdate
from config.oauth2 import get_current_super_admin, get_current_admin, get_current_active_user
from schemas.person.superadmin import SuperAdminGet
from schemas.person.person import PersonGet
from schemas.person.admin import AdminGet
from cruds.person.admin import get_admin_by_id
from fastapi import HTTPException, status


router = APIRouter(
    prefix="/institution",
    tags=["Institutions"]
)


@router.get("/", response_model=list[InstitutionGet])
def get_all_institutions(db: Session = Depends(get_db)):
    return crud_institution.get_all_institutions(db)

@router.get("/province/")
def get_all_institutions(db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_active_user)):
    return crud_institution.get_all_institution_labs(db, current_user.province_id)

@router.get("/laboratoryservices/{id}")
def get_all_laboratory_services(id: int, db: Session = Depends(get_db)):
    return crud_institution.get_institution_laboratories(db, id)


@router.post("/create", response_model=InstitutionGet)
async def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_institution.create_institution(db=db, institution=institution)


@router.patch("/update/{id}", response_model=InstitutionGet)
async def update_institution(institution: InstitutionUpdate, id: int, db: Session = Depends(get_db), current_user: PersonGet = Depends(get_current_admin)):
    if current_user.discriminator == "admin":
        admin = get_admin_by_id(db, current_user.id)
        if admin.institution_id != id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to update this institution"
            )

    return crud_institution.update_institution(db=db, institution=institution, id=id)


@router.delete("/delete/{id}", response_model=InstitutionGet)
async def delete_institution(id: int, db: Session = Depends(get_db), current_user: SuperAdminGet = Depends(get_current_super_admin)):
    return crud_institution.delete_institution(db=db, id=id)

# Rooms


@router.post("/rooms/create", response_model=RoomGet)
async def create_room(room: RoomCreate, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    if current_user.discriminator == "admin":
        room.institution_id = current_user.institution_id
    return crud_institution.add_institution_room(db=db, room_create=room)


@router.get("/rooms/", response_model=list[RoomGet])
async def get_rooms(type: int = 1, id: int = None, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    if current_user.discriminator == "admin":
        return crud_institution.get_institution_rooms(db=db, institution_id=current_user.institution_id, type = type)
    else:
        return crud_institution.get_institution_rooms(db=db, institution_id=id, type=type)

# Laboratories


@router.post("/laboratory/create")
async def create_laboratory(laboratory: LaboratoryServiceCreate, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    if current_user.discriminator == "admin":
        laboratory.institution_id = current_user.institution_id
    else:
        if laboratory.institution_id == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Institution id is required"
            )

    return crud_institution.add_institution_laboratory(db=db, laboratory_create=laboratory)


@router.get("/laboratory")
async def get_institution_laboratories(id: int = None, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    if current_user.discriminator == "admin":
        return crud_institution.get_institution_laboratories(db=db, institution_id=current_user.institution_id)
    else:
        return crud_institution.get_institution_laboratories(db=db, institution_id=id)


@router.get("/laboratory/name", response_model=list)
async def get_laboratories_by_name(name: Union[str, None] = None, db: Session = Depends(get_db)):
    return crud_institution.get_laboratories_by_name(db=db, name=name)

@router.delete("/laboratory/delete/{id}")
async def delete_laboratory(id: int, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
    return crud_institution.delete_laboratory(db=db, id=id)


# @router.patch("/laboratory/update/{id}", response_model=LaboratoryServiceGet)
# async def update_laboratory(laboratory: LaboratoryServiceUpdate, id: int, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
#     if current_user.discriminator == "admin":
#         laboratory.institution_id = current_user.institution_id
#     else: 
#         if laboratory.institution_id == None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Institution id is required"
#             )
#     return crud_institution.update_laboratory(db=db, laboratory_update=laboratory, id=id)

# @router.delete("/laboratory/delete/{id}", response_model=LaboratoryServiceGet)
# async def delete_laboratory(id: int, db: Session = Depends(get_db), current_user: AdminGet = Depends(get_current_admin)):
#     return crud_institution.delete_laboratory(db=db, id=id)
