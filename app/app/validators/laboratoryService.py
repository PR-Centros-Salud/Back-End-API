from sqlalchemy.orm import Session
from models.laboratoryService import LaboratoryService
from models.institution import Institution
from schemas.laboratoryService import (
    LaboratoryServiceCreate,
    LaboratoryServiceGet,
    LaboratoryServiceUpdate,
)
from validators.location import validate_location
from fastapi import HTTPException, status
from sqlalchemy import exc, and_
from validators.institution import validate_institution
from validators.person.medicalPersonal import validate_contract
from schemas.laboratoryService import LaboratoryServiceCreate


def validate_laboratory(
    db: Session, laboratory_create: LaboratoryServiceCreate
) -> bool:
    db_institution = validate_institution(db, laboratory_create.institution_id)
    db_contract = validate_contract(
        db, laboratory_create.medical_personal_id, laboratory_create.institution_id
    )

    if db_contract.is_lab_personal == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract does not allow for this personal to work in a laboratory",
        )

    if db_institution.institution_type in [1, 4]:
        if (
            db.query(LaboratoryService)
            .filter(
                and_(
                    LaboratoryService.laboratory_service_name
                    == laboratory_create.laboratory_service_name,
                    LaboratoryService.institution_id
                    == laboratory_create.institution_id,
                    LaboratoryService.status == 1,
                )
            )
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Laboratory Service already exists",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution is not valid for this operation.",
        )

    return True
