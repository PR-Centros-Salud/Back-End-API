from pydantic import validator, Field, EmailStr, BaseModel
from schemas.person.medicalPersonal import MedicalPersonalGet
from typing import Optional, List
from datetime import datetime, date


class LaboratoryServiceCreate(BaseModel):
    institution_id: int = Field(None, description="Institution id of the admin")
    laboratory_service_name: str = Field(..., description="Name of the laboratory")
    medical_personal_id: int = Field(
        None, description="Medical personal id of the person in charge of the laboratory service"
    )
    room_id : int = Field(..., description="Room id of the laboratory service")


class LaboratoryServiceGet(BaseModel):
    institution_id: int
    laboratory_service_name: str
    medical_personal: dict



class LaboratoryServiceUpdate(BaseModel):
    """LaboratoryServiceUpdate Schema"""

    laboratory_service_name: str = Field(..., description="Name of the laboratory")
