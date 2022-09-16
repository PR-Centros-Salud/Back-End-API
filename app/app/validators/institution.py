from sqlalchemy.orm import Session
from models.institution import Institution
from schemas.institution import InstitutionCreate
from validators.location import validate_location
from fastapi import HTTPException, status


def validate_create_institution(db: Session, institution: InstitutionCreate):
    db_institution = db.query(Institution).filter(
        Institution.address == institution.address).filter(Institution.status == 1).first()

    if db_institution:
        detail = "Institution already exists"

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    elif not validate_location(db, institution.province_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Province not found"
        )
    else:
        return institution
