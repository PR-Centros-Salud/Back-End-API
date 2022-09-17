from models.person.admin import Admin
from models.location import Province
from schemas.person.admin import AdminCreate, AdminGet, AdminUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.person.person import validate_create_person
from validators.location import validate_location
from cruds.person.person import delete_person


def create_admin(db: Session, admin: AdminCreate):
    try:
        admin = validate_create_person(db, admin)
        db_admin = Admin(**admin.dict())
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin error."
        )
    return db_admin


def update_admin(db: Session, admin: AdminUpdate, id: int):
    db_admin = db.query(Admin).filter(
        and_(Admin.id == id, Admin.status == 1)).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    if (admin.first_name):
        db_admin.first_name = admin.first_name
    if (admin.last_name):
        db_admin.last_name = admin.last_name
    if (admin.second_last_name):
        db_admin.second_last_name = admin.second_last_name
    if (admin.email):
        db_admin.email = admin.email
    if (admin.phone):
        db_admin.phone = admin.phone
    if (admin.address):
        db_admin.address = admin.address
    if (admin.province_id and validate_location(db, admin.province_id)):
        db_admin.province_id = admin.province_id
    db.commit()
    db.refresh(db_admin)
    return db_admin


def delete_admin(db: Session, id: int):
    db_admin = db.query(Admin).filter(
        and_(Admin.id == id, Admin.status == 1)).first()

    if not db_admin or not delete_person(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    db_admin.admin_status = 0
    db.commit()
    return db_admin
