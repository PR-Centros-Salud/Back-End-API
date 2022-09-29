from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class MedicalPersonalCreate(PersonCreate):
    """MedicalPersonalCreate Schema"""
    institution_id: int = Field(..., description="Institution id of the medicalPersonal")
    pass


class MedicalPersonalGet(PersonGet):
    """MedicalPersonalGet Schema"""
    # Add your fields here
    pass


class MedicalPersonalUpdate(PersonUpdate):
    """MedicalPersonalUpdate Schema"""
    # Add your fields here
    pass
