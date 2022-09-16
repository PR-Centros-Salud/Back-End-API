from models.person.superadmin import SuperAdmin
from models.location import Province
from schemas.person.superadmin import SuperAdminCreate, SuperAdminGet, SuperAdminUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.person import validate_create_person
from cruds.person.person import delete_person


def create_superadmin(db: Session, superadmin: SuperAdminCreate):
    try:
        superadmin = validate_create_person(db, superadmin)
        superadmin = superadmin.dict()
        superadmin.pop('creation_secret')
        db_superadmin = SuperAdmin(**superadmin)
        db.add(db_superadmin)
        db.commit()
        db.refresh(db_superadmin)
    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SuperAdmin error."
        )
    return db_superadmin


def update_superadmin(db: Session, superadmin: SuperAdminUpdate, id: int):
    db_superadmin = db.query(SuperAdmin).filter(
        and_(SuperAdmin.id == id, SuperAdmin.status == 1)).first()
    if not db_superadmin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SuperAdmin not found"
        )

    if (superadmin.first_name):
        db_superadmin.first_name = superadmin.first_name
    if (superadmin.last_name):
        db_superadmin.last_name = superadmin.last_name
    if (superadmin.second_last_name):
        db_superadmin.second_last_name = superadmin.second_last_name
    if (superadmin.email):
        db_superadmin.email = superadmin.email
    if (superadmin.phone):
        db_superadmin.phone = superadmin.phone
    if (superadmin.address):
        db_superadmin.address = superadmin.address
    if (superadmin.province_id):
        db_superadmin.province = superadmin.province
    db.commit()
    db.refresh(db_superadmin)
    return db_superadmin


def delete_superadmin(db: Session, id: int):
    db_superadmin = db.query(SuperAdmin).filter(
        and_(SuperAdmin.id == id, SuperAdmin.status == 1)).first()

    if not db_superadmin or not delete_person(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SuperAdmin not found"
        )

    db_superadmin.super_admin_status = 0
    db.commit()
    db.refresh(db_superadmin)
    return db_superadmin
