from typing import Union
from sqlalchemy.orm import Session
from schemas.person import client as client_schema
from models.person.person import Person
from models.location import Province
from validators.location import validate_location
from sqlalchemy import or_
from fastapi import HTTPException, status


def validate_create_person(db: Session, person: Union[client_schema.ClientCreate]):
    db_person = db.query(Person).filter(or_(Person.email == person.email, Person.username ==
                                            person.username, Person.identity_card == person.identity_card)).filter(Person.status == 1).first()

    if db_person:
        detail = "Person already exists"

        if db_person.email == person.email:
            detail = "Email already exists"
        elif db_person.username == person.username:
            detail = "Username already exists"
        else:
            detail = "Identity card already exists"

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    elif not validate_location(db, person.province_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Province not found"
        )
    else:
        return person