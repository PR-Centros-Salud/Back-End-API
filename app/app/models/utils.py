from config.database import Base


class Phone(Base):
    __tablename__ = 'phone'

    id = Column(Integer, primary_key=True)
    phone_reference = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    person = relationship('Person', back_populates='phone')
