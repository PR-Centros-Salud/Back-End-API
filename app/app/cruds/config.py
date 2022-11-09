from sqlalchemy.orm import Session
from models.location import Province


def get_available_provinces(db: Session):
    return db.query(Province).all()
