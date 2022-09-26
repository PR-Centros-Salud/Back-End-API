from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class MedicalPersonalCreate(PersonCreate):
    """MedicalPersonalCreate Schema"""
    # Add your fields here
    pass


class MedicalPersonalGet(PersonGet):
    """MedicalPersonalGet Schema"""
    # Add your fields here
    pass


class MedicalPersonalUpdate(PersonUpdate):
    """MedicalPersonalUpdate Schema"""
    # Add your fields here
    pass
