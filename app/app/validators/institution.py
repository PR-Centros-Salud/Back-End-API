from sqlalchemy.orm import Session
from models.institution import Institution, Room
from schemas.institution import InstitutionCreate, InstitutionGet, RoomCreate
from validators.location import validate_location
from fastapi import HTTPException, status
from sqlalchemy import exc, and_

def validate_create_institution(db: Session, institution: InstitutionCreate):
    if not validate_location(db, institution.province_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Province not found"
        )
    else:
        return institution


def validate_institution(db: Session, institution_id) -> Institution:
    db_institution = db.query(Institution).filter(
        and_(Institution.id == institution_id, Institution.status == 1)).first()

    if not db_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution not found"
        )

    return db_institution

def validate_create_room(db: Session, room: RoomCreate) -> bool:
    if room.room_block != None and room.room_floor != None:
        db_room = db.query(Room).filter(
            and_(Room.room_block == room.room_block, Room.room_floor == room.room_floor, Room.institution_id == room.institution_id, Room.room_number == room.room_number)).first()
    elif room.room_block != None:
        db_room = db.query(Room).filter(
            and_(Room.room_block == room.room_block, Room.institution_id == room.institution_id, Room.room_number == room.room_number)).first()
    elif room.room_floor != None:
        db_room = db.query(Room).filter(
            and_(Room.room_floor == room.room_floor, Room.institution_id == room.institution_id, Room.room_number == room.room_number)).first()
    else:
        db_room = db.query(Room).filter(
            and_(Room.institution_id == room.institution_id, Room.room_number == room.room_number)).first()
        
    if db_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room already exists"
        )
    return True
