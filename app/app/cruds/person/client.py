from models.person.client import Client
from schemas.person.client import ClientCreate, ClientGet, ClientUpdate, ClientUpdatePassword
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client: ClientUpdate, id: int):
    db_client = db.query(Client).filter(
        Client.id == id).first()
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


def update_client_password(db: Session, client: ClientUpdatePassword, id: int):
    db_client = db.query(Client).filter(
        Client.id == id).first()
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    if (client.password != client.confirm_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    if (db_client.verify_password(client.old_password)):
        db_client.password = client.new_password
        db.commit()
        db.refresh(db_client)
        return db_client
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )
    return db_client


def delete_client(db: Session, id: int):
    db_client = db.query(Client).filter(
        Client.id == id).first()
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    db_client.status = 0
    db.commit()
    return db_client
