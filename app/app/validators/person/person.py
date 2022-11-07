from typing import Union
from sqlalchemy.orm import Session
from schemas.person import (
    client as client_schema,
    admin as admin_schema,
    superadmin as superadmin_schema,
    medicalPersonal as medical_schema,
)

from models.person.person import Person
from models.location import Province
from validators.location import validate_location
from sqlalchemy import or_
from fastapi import HTTPException, status


def validate_create_person(
    db: Session,
    person: Union[
        client_schema.ClientCreate,
        admin_schema.AdminCreate,
        superadmin_schema.SuperAdminCreate,
        medical_schema.MedicalPersonalCreate,
    ],
):
    if type(person) == medical_schema.MedicalPersonalCreate:
        db_person = (
            db.query(Person)
            .filter(
                or_(
                    Person.email == person.email,
                    Person.phone == person.phone,
                    Person.identity_card == person.identity_card,
                )
            )
            .filter(Person.status == 1)
            .first()
        )
    else:
         db_person = (
            db.query(Person)
            .filter(
                or_(
                    Person.email == person.email,
                    Person.phone == person.phone,
                    Person.identity_card == person.identity_card,
                    Person.username == person.username,
                )
            )
            .filter(Person.status == 1)
            .first()
        )

    if db_person:
        detail = "Person already exists"

        if db_person.email == person.email:
            detail = "Email already exists"
        elif db_person.identity_card == person.identity_card:
            detail = "Identity card already exists"
        elif db_person.phone == person.phone:
            detail = "Phone already exists"
        else:
            detail = "Username already exists"

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    elif not validate_location(db, person.province_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Province not found"
        )
    else:
        return person
