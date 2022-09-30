from sqlalchemy.orm import Session
from models.person.medicalPersonal import MedicalPersonal, MedicalInstitution
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

def validate_medical_personal(db: Session, medical_id : int):
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
    else:
        return db_medicalPersonal

def validate_medical_institution(db: Session, medical_id: int, institution_id : int) -> bool:
    db_medicalPersonal = validate_medical_personal(db, medical_id)
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

    if db_medicalInstitution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active contract already exists",
        )
    else:
        return True