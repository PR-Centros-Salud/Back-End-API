# Library Importation
from models.person import Person
from schemas.person import PersonCreate, PersonGet

# SQLAlchemy
from sqlalchemy.orm import Session


def create_person(db: Session, person: PersonCreate):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_person_username(db: Session, username: str):
    db_person = db.query(Person).filter(
        Person.username == username).first()
    return db_person


def get_person_by_username(db: Session, username: str):
    db_person = db.query(Person).filter(
        Person.username == username).first()
    return db_person
