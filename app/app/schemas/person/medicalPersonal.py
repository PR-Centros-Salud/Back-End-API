from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class MedicalPersonalCreate(PersonCreate):
    """MedicalPersonalCreate Schema"""
    institution_id: int = Field(..., description="Institution id of the medicalPersonal")
    department : str = Field(..., description="Department of the medicalPersonal")
    role : str = Field(..., description="Role of the medicalPersonal")


class MedicalPersonalGet(PersonGet):
    """MedicalPersonalGet Schema"""
    # Add your fields here
    pass


class MedicalPersonalUpdate(PersonUpdate):
    """MedicalPersonalUpdate Schema"""
    # Add your fields here
    pass

class MedicalInstitutionCreate():
    """MedicalInstitution Schema"""
    department : str = Field(..., description="Department of the medicalPersonal")
    role : str = Field(..., description="Role of the medicalPersonal")
    institution_id: int = Field(..., description="Institution id of the medicalPersonal")
    medical_personal_id: int = Field(..., description="Medical personal id of the medicalPersonal")
