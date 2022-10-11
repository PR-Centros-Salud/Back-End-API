# Configs
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.location import Institution
from models.baseTable import BaseTable


class LaboratoryService(BaseTable):
    __tablename__ = 'laboratoryService'

    laboratory_service_name = Column(String(50), nullable=False)

    # Relationships
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False)