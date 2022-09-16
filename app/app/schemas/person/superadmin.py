import os
from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword
from dotenv import load_dotenv
load_dotenv()


class SuperAdminCreate(PersonCreate):
    creation_secret: str = Field(..., description="Secret of the superadmin",
                                 max_length=50, min_length=2)

    @validator('creation_secret')
    def validate_secret(cls, v):
        if v != os.getenv("SUPER_ADMIN_SECRET"):
            raise ValueError("Secret is not valid")
        return v
    """AdminCreate Schema"""
    # Add your fields here

    pass


class SuperAdminGet(PersonGet):
    """AdminGet Schema"""
    # Add your fields here
    pass


class SuperAdminUpdate(PersonUpdate):
    """AdminUpdate Schema"""
    # Add your fields here
    pass
