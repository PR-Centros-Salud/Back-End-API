# Library Importation
from models.baseTable import BaseTable

# Configs
from email.policy import default
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime


class Experience(BaseTable):
    __tablename__ = 'experiences'

    # Entity Fields
    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False)
    company = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(500), nullable=False)
