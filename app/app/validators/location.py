from sqlalchemy.orm import Session
from models.location import Province
from fastapi import HTTPException, status
from fastapi import HTTPException, status

def validate_location(db: Session, province_id) -> bool:
    db_province = db.query(Province).filter(
        Province.id == province_id).first()

    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Province not found"
        )

    return True
