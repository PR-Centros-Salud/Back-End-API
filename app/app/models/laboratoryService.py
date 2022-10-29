# Configs
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.baseTable import BaseTable


class LaboratoryService(BaseTable):
    __tablename__ = 'laboratory_service'

    laboratory_service_name = Column(String(50), nullable=False)

    # Relationships
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False)
    laboratory_appointment = relationship("LaboratoryAppointment", back_populates="laboratory_service")

