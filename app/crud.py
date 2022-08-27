from sqlalchemy.orm import Session
import models
import schemas


def create_experience(db: Session, experience: schemas.ExperienceCreate):
    db_experience = models.Experience(**experience.dict())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_person_username(db: Session, username: str):
    db_person = db.query(models.Person).filter(
        models.Person.username == username).first()
    return db_person


def get_person_by_username(db: Session, username: str):
    db_person = db.query(models.Person).filter(
        models.Person.username == username).first()
    return db_person
