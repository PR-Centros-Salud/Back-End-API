# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.person.person import Person
from models.institution import Institution


class Admin(Person):
    __tablename__ = 'admin'
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    # Entity Fields
    institution = relationship(
        "Institution", back_populates="admin", uselist=False)
