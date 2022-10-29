from pydantic import validator, Field, EmailStr, BaseModel
from typing import Optional, List
from datetime import datetime, date, time
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword
from enum import IntEnum

class Day(IntEnum):
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7



class ScheduleDayCreate(BaseModel):
    """ScheduleDayCreate Schema"""
    day : Day = Field(..., description="Day of the schedule")
    start_time: time = Field(..., description="Start time of the schedule")
    end_time: time = Field(..., description="End time of the schedule")
    room_id: int = Field(..., description="Room id of the schedule")

    class Config:
        orm_mode = True

class ScheduleCreate(BaseModel):
    """ScheduleCreate Schema"""
    estimated_appointment_time : int = Field(..., description="Estimated appointment time of the medicalPersonal")
    schedule_day_list : list[ScheduleDayCreate] = Field(..., description="Schedule day list of the medicalPersonal")

class MedicalPersonalCreate(PersonCreate):
    """MedicalPersonalCreate Schema"""
    institution_id: int = Field(..., description="Institution id of the medicalPersonal")
    department : str = Field(None, description="Department of the medicalPersonal")
    role : str = Field(..., description="Role of the medicalPersonal")
    schedule : ScheduleCreate = Field(..., description="Schedule of the medicalPersonal")

class MedicalPersonalGet(PersonGet):
    """MedicalPersonalGet Schema"""
    # Add your fields here
    pass


class MedicalPersonalUpdate(PersonUpdate):
    """MedicalPersonalUpdate Schema"""
    # Add your fields here
    pass

class ContractCreate(BaseModel):
    """ContractCreate Schema"""
    department : str = Field(None, description="Department of the medicalPersonal")
    role : str = Field(..., description="Role of the medicalPersonal")
    institution_id: int = Field(None, description="Institution id of the medicalPersonal")
    medical_personal_id: int = Field(..., description="Medical personal id of the medicalPersonal")
    schedule : ScheduleCreate = Field(..., description="Schedule of the medicalPersonal")


class SpecializationCreate(BaseModel):
    """SpecializationCreate Schema"""
    specialization_name : str = Field(..., description="Specialization name of the medicalPersonal")
    degree: str = Field(..., description="Name of the specialization")
    start_date: date = Field(..., description="Start date of the specialization")
    end_date: date = Field(..., description="End date of the specialization")
    location : str = Field(..., description="Location of the specialization")
    institution : str = Field(..., description="Institution of the specialization")

    class Config:
        orm_mode = True

class SpecializationGet(BaseModel):
    """SpecializationGet Schema"""
    specialization_name : str
    degree: str
    start_date: date
    end_date: date
    location : str
    institution : str
    degree_photo_url : str

    class Config:
        orm_mode = True

class SpecializationUpdate(BaseModel):
    """SpecializationUpdate Schema"""
    specialization_name : Optional[str] = Field(None, description="Specialization name of the medicalPersonal")
    degree: Optional[str] = Field(None, description="Name of the specialization")
    start_date: Optional[date] = Field(None, description="Start date of the specialization")
    end_date: Optional[date] = Field(None, description="End date of the specialization")
    location : Optional[str] = Field(None, description="Location of the specialization")
    institution : Optional[str] = Field(None, description="Institution of the specialization")

    class Config:
        orm_mode = True