from models.person.admin import Admin
from models.location import Province
from models.institution import Institution
from schemas.person.admin import AdminCreate, AdminGet, AdminUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.person.admin import validate_create_admin
from validators.location import validate_location
from cruds.person.person import delete_person
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from password_generator import PasswordGenerator
import phonenumbers
import os

load_dotenv()


def get_admin_by_id(db: Session, id: int):
    db_admin = db.query(Admin).filter(
        and_(Admin.id == id, Admin.status == 1)).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    db_institution = db.query(Institution).filter(
        and_(Institution.id == db_admin.institution_id, Institution.status == 1)).first()

    if not db_institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )

    db_admin.institution = db_institution
    return db_admin


def create_admin(db: Session, admin: AdminCreate):
    try:

        admin = validate_create_admin(db, admin)
        num = phonenumbers.parse(admin.phone, "BO")

        if not phonenumbers.is_valid_number(num):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is not valid.",
            )

        pwo = PasswordGenerator()
        pwo.maxlen = 16
        pwo.minlen = 8
        password = pwo.generate()

        admin.username = admin.email.split(
            "@")[0] + str(int(datetime.now().timestamp()))[5:]
        admin.password = password

        db_admin = Admin(**admin.dict())
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)

        client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                        os.getenv("TWILIO_AUTH_TOKEN"))
        body = (
            "\nWelcome to Medico, your account has been created successfully.\n\nYour username is: \n"
            + admin.username
            + "\nand your password is: \n"
            + password
        )
        message = client.messages.create(
            body=body, from_=os.getenv("TWILIO_NUMBER"), to=admin.phone
        )

    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin error."
        )
    return db_admin


def update_admin(db: Session, admin: AdminUpdate, id: int):
    db_admin = db.query(Admin).filter(
        and_(Admin.id == id, Admin.status == 1)).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    if (admin.first_name):
        db_admin.first_name = admin.first_name
    if (admin.last_name):
        db_admin.last_name = admin.last_name
    if (admin.second_last_name):
        db_admin.second_last_name = admin.second_last_name
    if (admin.email):
        db_admin.email = admin.email
    if (admin.phone):
        db_admin.phone = admin.phone
    if (admin.address):
        db_admin.address = admin.address
    if (admin.province_id and validate_location(db, admin.province_id)):
        db_admin.province_id = admin.province_id
    db.commit()
    db.refresh(db_admin)
    return db_admin


def delete_admin(db: Session, id: int):
    db_admin = db.query(Admin).filter(
        and_(Admin.id == id, Admin.status == 1)).first()

    if not db_admin or not delete_person(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    db_admin.admin_status = 0
    db.commit()
    return db_admin
