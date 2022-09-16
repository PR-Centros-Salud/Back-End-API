from models.person.client import Client
from models.location import Province
from models.person.person import Person
from schemas.person.client import ClientCreate, ClientGet, ClientUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.person import validate_create_person
from cruds.person.person import delete_person

def create_client(db: Session, client: ClientCreate):
    try:
        client = validate_create_person(db, client)
        db_client = Client(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client error."
        )
    return db_client


def update_client(db: Session, client: ClientUpdate, id: int):
    db_client = db.query(Client).filter(
        and_(Client.id == id, Client.status == 1)).first()
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    if (client.first_name):
        db_client.first_name = client.first_name
    if (client.last_name):
        db_client.last_name = client.last_name
    if (client.second_last_name):
        db_client.second_last_name = client.second_last_name
    if (client.email):
        db_client.email = client.email
    if (client.phone):
        db_client.phone = client.phone
    if (client.address):
        db_client.address = client.address
    if (client.province_id):
        db_client.province = client.province
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, id: int):
    db_client = db.query(Client).filter(
        and_(Client.id == id, Client.status == 1)).first()

    if not db_client or not delete_person(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    db_client.client_status = 0
    db.commit()
    return {"detail": "Client deleted successfully"}
