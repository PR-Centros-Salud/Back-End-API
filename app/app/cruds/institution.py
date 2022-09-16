from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from schemas.institution import InstitutionCreate, InstitutionGet, InstitutionUpdate
from validators.institution import validate_create_institution
from models.institution import Institution


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


# def update_institution(db: Session, institution: InstitutionUpdate, id: int):
#     db_institution = db.query(Institution).filter(
#         and_(Institution.id == id, Institution.status == 1)).first()
#     if not db_institution:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Institution not found"
#         )

#     if (institution.name):
#         db_institution.name = institution.name
#     if (institution.address):
#         db_institution.address = institution.address
#     if (institution.province_id and validate_location(db, institution.province_id)):
#         db_institution.province_id = institution.province_id

#     db.commit()
#     db.refresh(db_institution)
#     return db_institution
