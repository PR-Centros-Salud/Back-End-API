from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class ClientCreate(PersonCreate):
    """ClientCreate Schema"""
    # Add your fields here
    lat : float = Field(..., description="Latitude of the client")
    lng : float = Field(..., description="Longitude of the client")
    pass


class ClientGet(PersonGet):
    """ClientGet Schema"""
    # Add your fields here
    lat : float
    lng : float
    pass


class ClientUpdate(PersonUpdate):
    """ClientUpdate Schema"""
    # Add your fields here
    pass


class ClientUpdatePassword(PersonUpdatePassword):
    """ClientUpdatePassword Schema"""
    # Add your fields here
    pass
