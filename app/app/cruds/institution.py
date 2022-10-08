from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from schemas.institution import InstitutionCreate, InstitutionGet, InstitutionUpdate, RoomCreate
from validators.institution import validate_create_institution, validate_institution, validate_create_room
from models.institution import Institution, Room
from models.person.medicalPersonal import Contract
from models.person.admin import Admin
from models.person.person import Person
from datetime import datetime

def get_all_institutions(db: Session):
    return db.query(Institution).filter(Institution.status == 1).all()


def create_institution(db: Session, institution: InstitutionCreate):
    try:
        institution = validate_create_institution(db, institution)
        institution = institution.dict()
        institution["institution_type"] = institution["institution_type"].value
        db_institution = Institution(**institution)
        db.add(db_institution)
        db.commit()
        db.refresh(db_institution)
    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution error."
        )
    return db_institution


def update_institution(db: Session, institution: InstitutionUpdate, id: int):
    db_institution = validate_institution(db, id)

    if (institution.name):
        db_institution.name = institution.name
    if (institution.address):
        db_institution.address = institution.address
    if (institution.province_id and validate_location(db, institution.province_id)):
        db_institution.province_id = institution.province_id
    if (institution.phone):
        db_institution.phone = institution.phone
    if (institution.institution_type):
        db_institution.institution_type = institution.institution_type.value
    if (institution.latitude and institution.longitude):
        db_institution.latitude = institution.latitude
        db_institution.longitude = institution.longitude

    db.commit()
    db.refresh(db_institution)
    return db_institution


def delete_institution(db: Session, id: int):
    db_institution = validate_institution(db, id)

    db_institution.status = 0

    db_contract = db.query(Contract).filter(
        and_(Contract.institution_id == id, Contract.status == 1)).all()
    for contract in db_contract:
        contract.status = 0
        contract.end_date = datetime.now()

    db_admin = db.query(Admin).filter(
        and_(Admin.institution_id == id, Admin.status == 1)).all()
    for admin in db_admin:
        db_person = db.query(Person).filter(
            and_(Person.id == admin.id, Person.status == 1)).first()
        db_person.status = 0
        admin.admin_status = 0

    db_rooms = db.query(Room).filter(
        and_(Room.institution_id == id, Room.status == 1)).all()
    for room in db_rooms:
        room.status = 0

    db.commit()
    db.refresh(db_institution)
    return db_institution

def add_institution_room(db: Session, room_create: RoomCreate):
    db_institution = validate_institution(db, room_create.institution_id)
    if validate_create_room(db, room_create):
        room = room_create.dict()
        room["room_type"] = room["room_type"].value
        db_room = Room(**room)
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room

def get_institution_rooms(db: Session, institution_id: int):
    db_institution = validate_institution(db, institution_id)
    return db.query(Room).filter(and_(Room.institution_id == institution_id, Room.status == 1)).all()
