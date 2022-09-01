# Library Importation
from models.baseTable import BaseTable
from models.person.person import Person

# SQLAlchemy
from sqlalchemy import Column, Integer, String


class Client(Person):
    __tablename__ = "client"
    __mapper_args__ = {"polymorphic_identity": "client"}

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
