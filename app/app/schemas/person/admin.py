from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class AdminCreate(PersonCreate):
    institution_id: int = Field(..., description="Institution id of the admin")
    username: str = Field(...,
                          description="Username of the person", max_length=30, min_length=3)
    password: str = Field(...,
                          description="Password of the person", max_length=20)


class AdminGet(PersonGet):
    institution_id: int
    # Add your fields here


class AdminUpdate(PersonUpdate):
    """AdminUpdate Schema"""
    # Add your fields here
    pass
