from sqlalchemy.orm import Session
from models.location import Province
from fastapi import HTTPException, status


def validate_location(db: Session, province_id) -> bool:
    db_province = db.query(Province).filter(
        Province.id == province_id).first()
    if not db_province:
        return False
    else:
        return True
