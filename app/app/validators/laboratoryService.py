from sqlalchemy.orm import Session
from models.laboratoryService import LaboratoryService
from schemas.laboratoryService import LaboratoryServiceCreate, LaboratoryServiceGet, LaboratoryServiceUpdate
from validators.location import validate_location
from fastapi import HTTPException, status
from sqlalchemy import exc, and_

def validate_create_laboratory_service(db: Session, laboratoryService: LaboratoryService):
    if not validate_location(db, institution.province_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Province not found"
        )
    else:
        return institution


def validate_institution(db: Session, institution_id) -> Institution:
    db_institution = db.query(Institution).filter(
        and_(Institution.id == institution_id, Institution.status == 1)).first()

    if not db_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution not found"
        )

    return db_institution