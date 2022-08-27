# Library Importation
from models.experience import Experience
from schemas.experience import ExperienceCreate

# SQLAlchemy
from sqlalchemy.orm import Session


def create_experience(db: Session, experience: ExperienceCreate):
    db_experience = Experience(**experience.dict())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience
