from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime, date
from enum import IntEnum


class InstitutionType(IntEnum):
    health_center = 1
    consultory = 2
    pharmacy = 3
    laboratory = 4

class InstitutionCreate(BaseModel):
    name: str = Field(..., description="Name of the institution",
                      max_length=100)
    address: str = Field(...,
                         description="Address of the institution", max_length=100)
    phone: str = Field(...,
                       description="Phone of the institution", max_length=20)
    photo_url: Optional[str] = Field(
        None, description="Photo url of the institution", max_length=150)
    institution_type: InstitutionType = Field(
        ..., description="Type of the institution")
    latitude: float = Field(..., description="Latitude of the institution")
    longitude: float = Field(..., description="Longitude of the institution")
    province_id: int = Field(..., description="Province id of the institution")

    class Config:
        orm_mode = True


class InstitutionGet(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    photo_url: Optional[str] = None
    institution_type: InstitutionType
    latitude: float
    longitude: float
    province_id: int

    class Config:
        orm_mode = True


class InstitutionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the institution",
                                max_length=100)
    address: Optional[str] = Field(
        None, description="Address of the institution", max_length=100)
    phone: Optional[str] = Field(
        None, description="Phone of the institution", max_length=20)
    photo_url: Optional[str] = Field(
        None, description="Photo url of the institution", max_length=150)
    institution_type: Optional[int] = Field(
        None, description="Type of the institution")
    latitude: Optional[float] = Field(
        None, description="Latitude of the institution")
    longitude: Optional[float] = Field(
        None, description="Longitude of the institution")
    province_id: Optional[int] = Field(
        None, description="Province id of the institution")

    class Config:
        orm_mode = True
