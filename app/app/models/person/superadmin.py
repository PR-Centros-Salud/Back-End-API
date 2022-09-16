# SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from models.person.person import Person


class SuperAdmin(Person):
    __tablename__ = 'superadmin'
    __mapper_args__ = {'polymorphic_identity': 'superadmin'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    super_admin_created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    super_admin_updated_at = Column(DateTime, default=datetime.utcnow, nullable=False,
                                    onupdate=datetime.utcnow)
    super_admin_status = Column(SmallInteger, default=1, nullable=False)
