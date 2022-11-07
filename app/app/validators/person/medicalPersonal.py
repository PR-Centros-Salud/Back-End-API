from sqlalchemy.orm import Session
from models.person.medicalPersonal import MedicalPersonal, Contract, ScheduleDay
from models.institution import Room
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

def validate_medical_personal(db: Session, medical_id : int):
    db_medicalPersonal = (
        db.query(MedicalPersonal)
        .filter(
            and_(
                MedicalPersonal.id == medical_id,
                MedicalPersonal.medical_personal_status == 1,
            )
        )
        .first()
    )

    if not db_medicalPersonal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical Personal not found"
        )
    else:
        return db_medicalPersonal

def validate_contract(db: Session, medical_id: int, institution_id : int):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    db_contract = (
        db.query(Contract)
        .filter(
            and_(
                Contract.medical_personal_id == medical_id,
                Contract.institution_id == institution_id,
                Contract.status == 1,
            )
        )
        .first()
    )

    if db_contract:
        return db_contract
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")


def validate_schedule(db: Session, institution_id: int, schedule_day_list: list) -> bool:
    for schedule_day in schedule_day_list:
        validate_schedule_day(db, schedule_day.day.value, schedule_day.room_id, institution_id)
    return True

def validate_schedule_day(db: Session, day: int, room_id: int, institution_id: bool) -> bool:
    db_room = (
            db.query(Room)
            .filter(
                and_(
                    Room.id == room_id,
                    Room.status == 1,
                    Room.institution_id == institution_id,
                )
            )
            .first()
        )

    if not db_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room not found",
        )
    else:
        db_schedule = (
            db.query(ScheduleDay)
            .filter(
                and_(
                    ScheduleDay.room_id == room_id,
                    ScheduleDay.day == day,
                    ScheduleDay.status == 1,
                )
            )
            .first()
        )

        if db_schedule:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room is taken for that day",
            )

    return True