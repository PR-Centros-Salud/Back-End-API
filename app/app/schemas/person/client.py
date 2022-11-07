from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class ClientCreate(PersonCreate):
    """ClientCreate Schema"""
    username: str = Field(...,
                          description="Username of the person", max_length=30, min_length=3)
    password: str = Field(...,
                          description="Password of the person", max_length=20)
    lat : float = Field(..., description="Latitude of the client")
    lng : float = Field(..., description="Longitude of the client")


class ClientGet(PersonGet):
    """ClientGet Schema"""
    lat : float
    lng : float


class ClientUpdate(PersonUpdate):
    """ClientUpdate Schema"""
    lat : Optional[float] = Field(None, description="Latitude of the client")
    lng : Optional[float] = Field(None, description="Longitude of the client")


class ClientUpdatePassword(PersonUpdatePassword):
    """ClientUpdatePassword Schema"""
    # Add your fields here
    pass
