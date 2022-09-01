from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger

class Phone(Base):
    __tablename__ = 'phone'

    id = Column(Integer, primary_key=True)
    phone_reference = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    phone_type = Column(SmallInteger, nullable=False)

    # Relationships
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
