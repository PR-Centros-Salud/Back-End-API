from fastapi import APIRouter, Depends
from cruds import config as crud_config
from config.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/config",
    tags=["Config Endpoints"]
)


@router.get("/available-provinces")
def get_available_provinces(db: Session = Depends(get_db)):
    return crud_config.get_available_provinces(db)
