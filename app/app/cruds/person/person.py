# Library Importation
from fastapi import HTTPException, status
from models.person.person import Person
from schemas.person.person import PersonCreate, PersonGet, PersonUpdatePassword

# SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import and_


def create_person(db: Session, person: PersonCreate):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_person_username(db: Session, username: str):
    db_person = db.query(Person).filter(and_(
        Person.username == username, Person.status == 1)).first()
    return db_person


def get_person_by_username(db: Session, username: str):
    db_person = db.query(Person).filter(
        and_(Person.username == username, Person.status == 1)).first()
    return db_person


def update_password(db: Session, person: PersonUpdatePassword, id: int):
    db_person = db.query(Person).filter(
        Person.id == id).first()
    if not db_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    if (db_person.verify_password(person.old_password)):
        db_person.password = person.new_password
        db.commit()
        return {"detail": "Password updated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )


def delete_person(db: Session, id: int) -> bool:
    db_person = db.query(Person).filter(
        Person.id == id).first()

    if not db_person:
        return False

    db_person.status = 0
    db.commit()
    return True
