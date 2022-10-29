# Library Importation
from datetime import datetime
from models.baseTable import BaseTable
from models.person.person import Person
from sqlalchemy.orm import relationship

# SQLAlchemy
from sqlalchemy import Column, Integer, Float,  ForeignKey, DateTime, SmallInteger

class Client(Person):
    __tablename__ = "client"
    __mapper_args__ = {"polymorphic_identity": "client"}

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    lat = Column(Float(precision=32, decimal_return_scale=None), nullable=True)
    lng = Column(Float(precision=32, decimal_return_scale=None), nullable=True)
    client_created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    client_updated_at = Column(DateTime, default=datetime.utcnow, nullable=False,
                               onupdate=datetime.utcnow)
    client_status = Column(SmallInteger, default=1, nullable=False)

    appointment = relationship("Appointment", back_populates="client")
