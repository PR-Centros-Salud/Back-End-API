from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class AdminCreate(PersonCreate):
    institution_id: int = Field(..., description="Institution id of the admin")
    pass


class AdminGet(PersonGet):
    institution_id: int
    # Add your fields here
    pass


class AdminUpdate(PersonUpdate):
    """AdminUpdate Schema"""
    # Add your fields here
    pass
