# Library Importation
from pydantic import BaseModel, validator, Field, EmailStr
from typing import Optional
from datetime import datetime, date


class PersonCreate(BaseModel):
    first_name: str = Field(...,
                            description="First name of the person", max_length=50)
    last_name: str = Field(...,
                           description="Last name of the person", max_length=50)
    second_last_name: Optional[str] = Field(...,
                                            description="Second last name of the person", max_length=50)
    username: str = Field(...,
                          description="Username of the person", max_length=30)
    email: EmailStr = Field(..., description="Email of the person")
    password: str
    identity_card: str = Field(...,
                               description="Identity card of the person", max_length=30)
    address: str = Field(...,
                         description="Address of the person", max_length=50)
    gender: str = Field(..., max_length=1)
    birthdate: date = Field(..., description="Birthdate of the person")

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
