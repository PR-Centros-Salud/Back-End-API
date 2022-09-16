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
    institution_id = Column(Integer, ForeignKey("institution.id"))
    institution = relationship("Institution", back_populates="admin")

# {
#   "first_name": "string",
#   "last_name": "string",
#   "second_last_name": "string",
#   "username": "string",
#   "email": "user@example.com",
#   "password": "string",
#   "phone": "string",
#   "identity_card": "2312",
#   "address": "string",
#   "gender": "M",
#   "birthdate": "2022-09-15",
#   "province_id": 1
# }
