# Configs
from config.database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    state_name = Column(String(50), nullable=False)

    # Relationships
    province = relationship("Province")


class Province(Base):
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    province_name = Column(String(50), nullable=False, unique=True)

    # Relationships
    state_id = Column(Integer, ForeignKey('state.id'), nullable=False)
    person = relationship('Person',
                          # back_populates='province'
                          )
