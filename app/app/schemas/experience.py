# Library Importation
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date


class ExperienceCreate(BaseModel):
    role: str
    company: str
    location: str
    start_date: date
    end_date: date
    description: str

    class Config:
        orm_mode = True
