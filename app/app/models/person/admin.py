# SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from models.person.person import Person
from models.institution import Institution


class Admin(Person):
    __tablename__ = 'admin'
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    # Entity Fields
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    admin_created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    admin_updated_at = Column(DateTime, default=datetime.utcnow, nullable=False,
                              onupdate=datetime.utcnow)
    admin_status = Column(SmallInteger, default=1, nullable=False)

    # Relationships
    institution_id = Column(Integer, ForeignKey(
        "institution.id"), nullable=False)
    institution = relationship("Institution", back_populates="admin")

