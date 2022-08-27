from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date


# class Country(BaseModel):
#     id: int
#     name: str


# class State(BaseModel):
#     id: int
#     name: str
#     country_id: int


class ExperienceCreate(BaseModel):
    role: str
    company: str
    location: str
    start_date: date
    end_date: date
    description: str

    class Config:
        orm_mode = True


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

# Auth


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
