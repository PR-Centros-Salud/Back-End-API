from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date


class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    second_last_name: Optional[str] = None
    username: str
    email: str
    password: str
    identity_card: str
    address: str
    gender: str
    birthdate: date

    class Config:
        orm_mode = True


class PersonGet(BaseModel):
    id: int
    first_name: str
    last_name: str
    second_last_name: Optional[str] = None
    username: str
    email: str
    identity_card: str
    address: str
