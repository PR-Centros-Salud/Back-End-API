# Library Importation
# Configs
from email.policy import default
from config.database import Base
from datetime import datetime

# SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger, DateTime


class BaseTable(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    status = Column(SmallInteger, default=True)
