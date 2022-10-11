from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.institution.institution import InstitutionCreate, InstitutionGet, InstitutionUpdate


class LaboratoryServiceCreate(InstitutionCreate):
    institution_id: int = Field(..., description="Institution id of the admin")
    laboratory_service_name: str = Field(..., description="Name of the laboratory")
    pass


class LaboratoryServiceGet(InstitutionGet):
    institution_id: int
    laboratory_service_name: str
    # Add your fields here
    pass


class LaboratoryServiceUpdate(InstitutionUpdate):
    """LaboratoryServiceUpdate Schema"""
    laboratory_service_name: str = Field(..., description="Name of the laboratory")
    # Add your fields here
    pass
