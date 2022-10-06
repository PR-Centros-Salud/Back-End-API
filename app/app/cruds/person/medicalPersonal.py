from models.person.medicalPersonal import MedicalPersonal, Specialization
from datetime import datetime
from models.person.person import Person
from models.person.medicalPersonal import Contract
from schemas.person.medicalPersonal import (
    MedicalPersonalCreate,
    MedicalPersonalGet,
    MedicalPersonalUpdate,
    ContractCreate,
    SpecializationCreate,
    SpecializationUpdate,
)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.institution import validate_institution
from validators.person.person import validate_create_person
from validators.person.medicalPersonal import validate_medical_personal
from cruds.person.person import delete_person


def create_MedicalPersonal(db: Session, medicalPersonal: MedicalPersonalCreate):
    try:
        medicalPersonal = validate_create_person(db, medicalPersonal)
        medicalPersonal = medicalPersonal.dict()

        contract = dict()
        contract["institution_id"] = medicalPersonal.pop("institution_id")
        validate_institution(db, contract["institution_id"])

        contract["department"] = medicalPersonal.pop("department")
        contract["role"] = medicalPersonal.pop("role")
        db_medicalPersonal = MedicalPersonal(**medicalPersonal)
        db.add(db_medicalPersonal)
        db.commit()
        db.refresh(db_medicalPersonal)
        contract["medical_personal_id"] = db_medicalPersonal.id
        create_medical_contract(db, contract)

    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Medical Personal error."
        )
    return db_medicalPersonal


def create_medical_contract(db: Session, contract: ContractCreate):
    try:
        if validate_institution(db, contract["institution_id"]) != None:
            db_contract = Contract(**contract)
            db.add(db_contract)
            db.commit()
            db.refresh(db_contract)
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
    return db_contract


def update_MedicalPersonal(
    db: Session, medicalPersonal: MedicalPersonalUpdate, id: int
):
    db_medicalPersonal = validate_medical_personal(db, id)

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
    db_medicalPersonal = validate_medical_personal(db, medical_id)

    db_contract = (
        db.query(Contract)
        .filter(
            and_(
                Contract.medical_personal_id == medical_id,
                Contract.institution_id == institution_id,
                Contract.status == 1,
            )
        )
        .first()
    )

    if not db_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal in Institution not found",
        )

    db_contract.status = 0
    db_contract.end_date = datetime.utcnow()
    db.commit()
    db.refresh(db_contract)
    return {"detail": "Medical Personal removed successfully"}


def get_contracts(db: Session, id: int):
    db_medicalPersonal = validate_medical_personal(db, id)

    db_contract = (
        db.query(Contract)
        .filter(
            and_(
                Contract.medical_personal_id == id,
                Contract.status == 1,
            )
        )
        .all()
    )
    return db_contract


def get_specializations(db: Session, id: int):
    db_medicalPersonal = validate_medical_personal(db, id)

    db_specializations = (
        db.query(Specialization)
        .filter(
            and_(
                Specialization.medical_personal_id == id,
                Specialization.status == 1,
            )
        )
        .all()
    )
    return db_specializations


def add_specialization(
    db: Session, specialization: SpecializationCreate, medical_id: int
):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    specialization = specialization.dict()
    specialization["medical_personal_id"] = medical_id
    db_specialization = Specialization(**specialization)
    db.add(db_specialization)
    db.commit()
    db.refresh(db_specialization)
    return db_specialization


def update_specialization(
    db: Session,
    specialization_id: int,
    specialization: SpecializationUpdate,
    medical_id: int,
):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    db_specialization = (
        db.query(Specialization)
        .filter(
            and_(
                Specialization.medical_personal_id == medical_id,
                Specialization.id == specialization_id,
                Specialization.status == 1,
            )
        )
        .first()
    )

    if not db_specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )

    if specialization.specialization_name:
        db_specialization.specialization_name = specialization.specialization_name
    if specialization.degree:
        db_specialization.degree = specialization.degree
    if specialization.institution:
        db_specialization.institution = specialization.institution
    if specialization.start_date:
        db_specialization.start_date = specialization.start_date
    if specialization.end_date:
        db_specialization.end_date = specialization.end_date
    if specialization.location:
        db_specialization.location = specialization.location
    db.commit()
    db.refresh(db_specialization)
    return db_specialization


def delete_specialization(db: Session, specialization_id: int, medical_id: int):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    db_specialization = (
        db.query(Specialization)
        .filter(
            and_(
                Specialization.medical_personal_id == medical_id,
                Specialization.id == specialization_id,
                Specialization.status == 1,
            )
        )
        .first()
    )

    if not db_specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )

    db_specialization.status = 0
    db.commit()
    db.refresh(db_specialization)
    return {"detail": "Specialization deleted successfully"}
