from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class AdminCreate(PersonCreate):
    """AdminCreate Schema"""
    # Add your fields here
    pass


class AdminGet(PersonGet):
    """AdminGet Schema"""
    # Add your fields here
    pass


class AdminUpdate(PersonUpdate):
    """AdminUpdate Schema"""
    # Add your fields here
    pass
