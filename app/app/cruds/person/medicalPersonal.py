from models.person.medicalPersonal import MedicalPersonal
from datetime import datetime
from models.person.person import Person
from models.person.medicalPersonal import MedicalInstitution
from schemas.person.medicalPersonal import (
    MedicalPersonalCreate,
    MedicalPersonalGet,
    MedicalPersonalUpdate,
    MedicalInstitutionCreate,
)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.institution import validate_institution
from validators.person.person import validate_create_person
from cruds.person.person import delete_person


def create_MedicalPersonal(db: Session, medicalPersonal: MedicalPersonalCreate):
    try:
        medicalPersonal = validate_create_person(db, medicalPersonal)
        medicalPersonal = medicalPersonal.dict()

        medicalInstitution = dict()
        medicalInstitution["institution_id"] = medicalPersonal.pop("institution_id")
        validate_institution(db, medicalInstitution["institution_id"])

        medicalInstitution["department"] = medicalPersonal.pop("department")
        medicalInstitution["role"] = medicalPersonal.pop("role")
        db_medicalPersonal = MedicalPersonal(**medicalPersonal)
        db.add(db_medicalPersonal)
        db.commit()
        db.refresh(db_medicalPersonal)
        medicalInstitution["medical_personal_id"] = db_medicalPersonal.id
        create_medical_contract(db, medicalInstitution)

    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Medical Personal error."
        )
    return db_medicalPersonal


def create_medical_contract(db: Session, medical_institution: MedicalInstitutionCreate):
    try:
        if validate_institution(db, medical_institution["institution_id"]):
            db_medical_institution = MedicalInstitution(**medical_institution)
            db.add(db_medical_institution)
            db.commit()
            db.refresh(db_medical_institution)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Institution not found"
            )
    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Medical Institution error."
        )
    return db_medical_institution


def update_MedicalPersonal(
    db: Session, medicalPersonal: MedicalPersonalUpdate, id: int
):
    db_medicalPersonal = (
        db.query(MedicalPersonal)
        .filter(
            and_(MedicalPersonal.id == id, MedicalPersonal.medical_personal_status == 1)
        )
        .first()
    )
    if not db_medicalPersonal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical Personal not found"
        )

    if medicalPersonal.first_name:
        db_medicalPersonal.first_name = medicalPersonal.first_name
    if medicalPersonal.last_name:
        db_medicalPersonal.last_name = medicalPersonal.last_name
    if medicalPersonal.second_last_name:
        db_medicalPersonal.second_last_name = medicalPersonal.second_last_name
    if medicalPersonal.email:
        db_medicalPersonal.email = medicalPersonal.email
    if medicalPersonal.phone:
        db_medicalPersonal.phone = medicalPersonal.phone
    if medicalPersonal.address:
        db_medicalPersonal.address = medicalPersonal.address
    if medicalPersonal.province_id and validate_location(
        db, medicalPersonal.province_id
    ):
        db_medicalPersonal.province_id = medicalPersonal.province_id
    db.commit()
    db.refresh(db_medicalPersonal)
    return db_medicalPersonal


def remove_medicalPersonal(db: Session, medical_id: int, institution_id: int):
    db_medicalPersonal = (
        db.query(MedicalPersonal)
        .filter(
            and_(
                MedicalPersonal.id == medical_id,
                MedicalPersonal.medical_personal_status == 1,
            )
        )
        .first()
    )

    if not db_medicalPersonal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical Personal not found"
        )

    db_medicalInstitution = (
        db.query(MedicalInstitution)
        .filter(
            and_(
                MedicalInstitution.medical_personal_id == medical_id,
                MedicalInstitution.institution_id == institution_id,
                MedicalInstitution.status == 1,
            )
        )
        .first()
    )

    if not db_medicalInstitution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal in Institution not found",
        )

    db_medicalInstitution.status = 0
    db_medicalInstitution.end_date = datetime.utcnow()
    db.commit()
    db.refresh(db_medicalInstitution)
    return {"detail": "Medical Personal removed successfully"}


def get_contracts(db: Session, id: int):
    db_medicalPersonal = (
        db.query(MedicalPersonal)
        .filter(and_(MedicalPersonal.id == id, MedicalPersonal.status == 1))
        .first()
    )

    if not db_medicalPersonal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical Personal not found"
        )

    db_medicalInstitution = (
        db.query(MedicalInstitution)
        .filter(
            and_(
                MedicalInstitution.medical_personal_id == id,
                MedicalInstitution.status == 1,
            )
        )
        .all()
    )
    return db_medicalInstitution
