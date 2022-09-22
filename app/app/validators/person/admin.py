from validators.person.person import validate_create_person
from validators.institution import validate_institution
from schemas.person import admin as admin_schema
from sqlalchemy.orm import Session


def validate_create_admin(db: Session, admin: admin_schema.AdminCreate):
    valid_person = validate_create_person(db, admin)
    if validate_institution(db, admin.institution_id):
        return valid_person
