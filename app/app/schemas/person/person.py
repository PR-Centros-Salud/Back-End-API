# Library Importation
from pydantic import BaseModel, validator, Field, EmailStr
from typing import Optional
from datetime import datetime, date


class PersonCreate(BaseModel):
    first_name: str = Field(...,
                            description="First name of the person", max_length=50, min_length=2)
    last_name: str = Field(...,
                           description="Last name of the person", max_length=50, min_length=2)
    second_last_name: Optional[str] = Field(None,
                                            description="Second last name of the person", max_length=50, min_length=2)
    email: EmailStr = Field(..., description="Email of the person")
    phone: str = Field(...,
                       description="Phone of the person", max_length=20)
    identity_card: str = Field(...,
                               description="Identity card of the person", max_length=30)
    address: str = Field(...,
                         description="Address of the person", max_length=50, min_length=2)
    gender: str = Field(..., description="Gender of the person", max_length=1)
    birthdate: date = Field(..., description="Birthdate of the person")
    province_id: int = Field(..., description="Province id of the person")

    @validator('birthdate')
    def validate_birthdate(cls, v):
        if v > datetime.now().date():
            raise ValueError("Birthdate must be less than now")
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['M', 'F', 'U']:
            raise ValueError("Gender is not valid")
        return v

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
    phone: str
    gender: str
    address: str
    discriminator: str
    province_id: int

    class Config:
        orm_mode = True


class PersonUpdate(BaseModel):
    first_name: Optional[str] = Field(None,
                                      description="First name of the person", max_length=50)
    last_name: Optional[str] = Field(None,
                                     description="Last name of the person", max_length=50)
    second_last_name: Optional[str] = Field(None,
                                            description="Second last name of the person", max_length=50)
    email: Optional[EmailStr] = Field(None, description="Email of the person")

    phone: Optional[str] = Field(None,
                                 description="Phone of the person", max_length=20)
    gender: Optional[str] = Field(None,
                                  description="Gender of the person", max_length=1)
    address: Optional[str] = Field(None,
                                   description="Address of the person", max_length=50)
    province_id: Optional[int] = Field(None,
                                       description="Province id of the person")

    class Config:
        orm_mode = True

class PersonUpdatePassword(BaseModel):
    old_password: str
    new_password: str

    class Config:
        orm_mode = True
