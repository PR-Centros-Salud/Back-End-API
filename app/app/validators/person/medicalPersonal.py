from sqlalchemy.orm import Session
from models.person.medicalPersonal import MedicalPersonal
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