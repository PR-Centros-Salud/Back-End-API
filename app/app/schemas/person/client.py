from pydantic import validator, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from schemas.person.person import PersonCreate, PersonGet, PersonUpdate, PersonUpdatePassword


class ClientCreate(PersonCreate):
    """ClientCreate Schema"""
    # Add your fields here
    pass


class ClientGet(PersonGet):
    """ClientGet Schema"""
    # Add your fields here
    pass


class ClientUpdate(PersonUpdate):
    """ClientUpdate Schema"""
    # Add your fields here
    pass


class ClientUpdatePassword(PersonUpdatePassword):
    """ClientUpdatePassword Schema"""
    # Add your fields here
    pass
