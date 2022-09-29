from models.person.medicalPersonal import MedicalPersonal
from models.person.person import Person
from schemas.person.medicalPersonal import MedicalPersonalCreate, MedicalPersonalGet, MedicalPersonalUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.person.person import validate_create_person
from cruds.person.person import delete_person

def create_MedicalPersonal(db: Session, medicalPersonal: MedicalPersonalCreate):
    try:
        medicalPersonal = validate_create_person(db, medicalPersonal)
        medicalPersonal = medicalPersonal.dict()
        instution_id = medicalPersonal.pop("institution_id")
        print(instution_id)
        db_medicalPersonal = MedicalPersonal(**medicalPersonal)
        db.add(db_medicalPersonal)
        db.commit()
        db.refresh(db_medicalPersonal)
    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medical Personal error."
        )
    return db_medicalPersonal


def update_MedicalPersonal(db: Session, medicalPersonal: MedicalPersonalUpdate, id: int):
    print('sap')
    db_medicalPersonal = db.query(MedicalPersonal).filter(
        and_(MedicalPersonal.id == id, MedicalPersonal.medical_personal_status == 1)).first()
    if not db_medicalPersonal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal not found"
        )

    if (medicalPersonal.first_name):
        db_medicalPersonal.first_name = medicalPersonal.first_name
    if (medicalPersonal.last_name):
        db_medicalPersonal.last_name = medicalPersonal.last_name
    if (medicalPersonal.second_last_name):
        db_medicalPersonal.second_last_name = medicalPersonal.second_last_name
    if (medicalPersonal.email):
        db_medicalPersonal.email = medicalPersonal.email
    if (medicalPersonal.phone):
        db_medicalPersonal.phone = medicalPersonal.phone
    if (medicalPersonal.address):
        db_medicalPersonal.address = medicalPersonal.address
    if (medicalPersonal.province_id and validate_location(db, medicalPersonal.province_id)):
        db_medicalPersonal.province_id = medicalPersonal.province_id
    db.commit()
    db.refresh(db_medicalPersonal)
    return db_medicalPersonal


def delete_medicalPersonal(db: Session, id: int):
    db_medicalPersonal = db.query(MedicalPersonal).filter(
        and_(MedicalPersonal.id == id, MedicalPersonal.status == 1)).first()

    if not db_medicalPersonal or not delete_person(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal not found"
        )
    db_medicalPersonal.medicalPersonal_status = 0
    db.commit()
    return {"detail": "Medical Personal deleted successfully"}
