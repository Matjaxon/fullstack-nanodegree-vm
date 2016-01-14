from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# association_table = Table('association', Base.metadata,\
# Column('puppy_id', Integer, ForeignKey('puppy.id')),\
# Column('adopter_id', Integer, ForeignKey('adopter.id')))

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    capacity = Column(Integer, nullable = False)
    remaining_capacity = Column(Integer)

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship('Shelter')
    weight = Column(Numeric(10))
    profile = relationship('PuppyProfile')
    adopter_id = Column(Integer, ForeignKey('adopter.id'))
    adopter_name = relationship('Adopter')
    adoption_date = Column(Date)

class PuppyProfile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'), unique = True)
    picture = relationship(Puppy)
    puppy_desc = Column(String)
    needs = Column(String(250))

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    dateOfBirth = Column(Date)

engine = create_engine('postgresql:///puppyshelter')

Base.metadata.create_all(engine)
