# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    SmallInteger,
    Float,
)
from sqlalchemy.orm import relationship
from schemas.institution import InstitutionType


class Institution(BaseTable):
    __tablename__ = "institution"

    # Entity Fields
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    photo_url = Column(String(150), nullable=True)
    institution_type = Column(SmallInteger, nullable=False)
    latitude = Column(Float(precision=32, decimal_return_scale=None), nullable=False)
    longitude = Column(Float(precision=32, decimal_return_scale=None), nullable=False)

    # Relationships
    admin = relationship("Admin", back_populates="institution")
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    contract = relationship("Contract", back_populates="institution")
    room = relationship("Room", back_populates="institution")
    
    appointments = relationship("Appointment", back_populates="institution")

class Room(BaseTable):
    __tablename__ = "room"

    # Entity Fields
    room_type = Column(SmallInteger, nullable=False)
    room_number = Column(String(10), nullable=False)
    room_floor = Column(String(10), nullable=True)
    room_block = Column(String(10), nullable=True)

    # Relationships
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False)
    institution = relationship("Institution", back_populates="room")

    schedule_day = relationship("ScheduleDay", back_populates="room")
    appointments = relationship("Appointment", back_populates="room")

