from pydantic import BaseModel, validator, Field, EmailStr
from typing import Optional
from datetime import datetime, date, time

class AppointmentCreate(BaseModel):
    programmed_date : date = Field(..., description="Programmed date of the appointment")
    medical_personal_id : int = Field(..., description="Medical personal id")
    patient_id : int = Field(None, description="Patient id")
    institution_id : int = Field(..., description="Institution id")
    schedule_day_appointment_id : int = Field(..., description="Schedule day appointment id")

    @validator('programmed_date')
    def validate_programmed_date(cls, v):
        if v < date.today():
            raise ValueError('Programmed date must be greater or equal to today')
        return v

    class Config:
        orm_mode = True

class AppointmentGet(BaseModel):
    institution_id: int ## REVISAR POR DONDE EL LLAMADO
    # Add your fields here
    pass


class AppointmentUpdate(BaseModel):
    programmed_date : date = Field(..., description="Programmed date of the appointment")
    start_time : time = Field(..., description="Start time of the appointment")
    end_time : time = Field(..., description="End time of the appointment")
    medical_personal_id : int = Field(..., description="Medical personal id")
    room_id : int = Field(..., description="Room id")
    patient_id : int = Field(..., description="Patient id")
    institution_id : int = Field(..., description="Institution id")

    @validator('programmed_date')
    def validate_programmed_date(cls, v):
        if v < date.today():
            raise ValueError('Programmed date must be greater than today')
        return v

class MedicalAppointmentCreate(AppointmentCreate):
    pass

class LaboratoryAppointmentCreate(AppointmentCreate):
    laboratory_service_id : int = Field(..., description="Laboratory service id")


class MedicalAppointmentFinished(BaseModel):
    recipe: str = Field(None, description="Recipe of the appointment")

class LaboratoryAppointmentFinished(BaseModel):
    result: str = Field(None, description="Result of the appointment")
    delivery_datetime: datetime = Field(..., description="Delivery datetime of the appointment")