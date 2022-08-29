# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    state_name = Column(String(50), nullable=False)


class Province(Base):
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    province_name = Column(String(50), nullable=False)
    state_id = Column(Integer, ForeignKey('state.id'), nullable=False)
    state = relationship('State', back_populates='provinces')
    person = relationship('Person', back_populates='province')
