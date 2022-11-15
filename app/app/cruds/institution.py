from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from schemas.institution import (
    InstitutionCreate,
    InstitutionGet,
    InstitutionUpdate,
    RoomCreate,
)
from schemas.laboratoryService import (
    LaboratoryServiceCreate,
    LaboratoryServiceGet,
    LaboratoryServiceUpdate,
)
from validators.institution import (
    validate_create_institution,
    validate_institution,
    validate_create_room,
)
from validators.laboratoryService import validate_laboratory
from models.laboratoryService import LaboratoryService
from models.institution import Institution, Room
from models.person.medicalPersonal import Contract, MedicalPersonal
from models.person.admin import Admin
from models.person.person import Person
from datetime import datetime
from validators.location import validate_location


def get_all_institution_labs(db: Session, province_id: int):
    db_province = validate_location(db, province_id)
    db_institutions = (
        db.query(Institution)
        .filter(
            and_(
                Institution.province_id == province_id,
                or_(
                    Institution.institution_type == 1, Institution.institution_type == 4
                ),
            )
        )
        .all()
    )

    institutions = []

    for institution in db_institutions:
        institution.laboratories = (
            db.query(LaboratoryService)
            .filter(
                and_(
                    LaboratoryService.institution_id == institution.id,
                    LaboratoryService.status == 1,
                )
            )
            .all()
        )

        if len(institution.laboratories) >= 1:

            for laboratory in institution.laboratories:
                laboratory.room = (
                    db.query(Room)
                    .filter(
                        and_(
                            Room.id == laboratory.room_id,
                            Room.status == 1,
                        )
                    )
                    .first()
                )
                laboratory.medical_personal = (
                    db.query(MedicalPersonal)
                    .filter(
                        and_(
                            MedicalPersonal.id == laboratory.medical_personal_id,
                            MedicalPersonal.status == 1,
                        )
                    )
                    .first()
                )
            institutions.append(institution)

    return institutions


def get_institution_laboratories(db: Session, institution_id: int):
    db_institution = validate_institution(db, institution_id)
    db_laboratories = (
        db.query(LaboratoryService)
        .filter(
            and_(
                LaboratoryService.institution_id == institution_id,
                LaboratoryService.status == 1,
            )
        )
        .all()
    )
    for laboratory in db_laboratories:
        laboratory.medical_personal = (
            db.query(MedicalPersonal)
            .filter(
                and_(
                    MedicalPersonal.id == laboratory.medical_personal_id,
                    MedicalPersonal.status == 1,
                )
            )
            .first()
        )
    return db_laboratories


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
            status_code=status.HTTP_400_BAD_REQUEST, detail="Institution error."
        )
    return db_institution


def update_institution(db: Session, institution: InstitutionUpdate, id: int):
    db_institution = validate_institution(db, id)
    print(institution)

    if institution.name:
        db_institution.name = institution.name
    if institution.address:
        db_institution.address = institution.address
    if institution.province_id and validate_location(db, institution.province_id):
        db_institution.province_id = institution.province_id
    if institution.phone:
        db_institution.phone = institution.phone
    if institution.institution_type:
        db_institution.institution_type = institution.institution_type.value
    if institution.latitude and institution.longitude:
        db_institution.latitude = institution.latitude
        db_institution.longitude = institution.longitude

    db.commit()
    db.refresh(db_institution)
    return db_institution


def delete_institution(db: Session, id: int):
    db_institution = validate_institution(db, id)

    db_institution.status = 0

    db_contract = (
        db.query(Contract)
        .filter(and_(Contract.institution_id == id, Contract.status == 1))
        .all()
    )
    for contract in db_contract:
        contract.status = 0
        contract.end_date = datetime.now()

    db_admin = (
        db.query(Admin)
        .filter(and_(Admin.institution_id == id, Admin.status == 1))
        .all()
    )
    for admin in db_admin:
        db_person = (
            db.query(Person)
            .filter(and_(Person.id == admin.id, Person.status == 1))
            .first()
        )
        db_person.status = 0
        admin.admin_status = 0

    db_rooms = (
        db.query(Room).filter(and_(Room.institution_id == id, Room.status == 1)).all()
    )
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


def get_institution_rooms(db: Session, institution_id: int, type: int):
    db_institution = validate_institution(db, institution_id)
    if type == 3:
        return (
            db.query(Room)
            .filter(and_(Room.institution_id == institution_id, Room.status == 1))
            .all()
        )
    else:
        return (
            db.query(Room)
            .filter(
                and_(
                    Room.institution_id == institution_id,
                    Room.status == 1,
                    Room.room_type == type,
                )
            )
            .all()
        )


def add_institution_laboratory(db: Session, laboratory_create: LaboratoryServiceCreate):
    if validate_laboratory(db, laboratory_create):
        laboratory = laboratory_create.dict()
        db_laboratory = LaboratoryService(**laboratory)
        db.add(db_laboratory)
        db.commit()
        db.refresh(db_laboratory)
        db_laboratory.medical_personal = (
            db.query(MedicalPersonal)
            .filter(
                and_(
                    MedicalPersonal.id == db_laboratory.medical_personal_id,
                    MedicalPersonal.status == 1,
                )
            )
            .first()
        )

        return db_laboratory


def get_institution_laboratories(db: Session, institution_id: int):
    db_institution = validate_institution(db, institution_id)
    db_lab_services = (
        db.query(LaboratoryService)
        .filter(
            and_(
                LaboratoryService.institution_id == institution_id,
                LaboratoryService.status == 1,
            )
        )
        .all()
    )
    for lab_service in db_lab_services:
        lab_service = lab_service.__dict__
        lab_service["medical_personal"] = (
            db.query(MedicalPersonal)
            .filter(
                and_(
                    MedicalPersonal.id == lab_service["medical_personal_id"],
                    MedicalPersonal.status == 1,
                )
            )
            .first()
            .__dict__
        )
        lab_service["medical_personal"].pop("_password")
        lab_service["medical_personal"].pop("status")
        lab_service["medical_personal"].pop("medical_personal_status")
        lab_service["medical_personal"].pop("medical_personal_updated_at")
        lab_service["medical_personal"].pop("medical_personal_created_at")
        lab_service["room"] = (
            db.query(Room)
            .filter(and_(Room.id == lab_service["room_id"], Room.status == 1))
            .first()
            .__dict__
        )

    return db_lab_services


def get_laboratories_by_name(db: Session, name: str):
    return (
        db.query(LaboratoryService)
        .filter(
            and_(
                LaboratoryService.laboratory_service_name == name,
                LaboratoryService.status == 1,
            )
        )
        .all()
    )


def delete_laboratory(db: Session, id: int):
    db_laboratory = validate_laboratory(db, id)
    db_laboratory.status = 0
    db.commit()
    db.refresh(db_laboratory)
    return db_laboratory
