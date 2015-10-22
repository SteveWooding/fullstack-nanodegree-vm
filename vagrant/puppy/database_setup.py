#!/usr/bin/env python
"""Setup a database of puppies and dog shelters"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    """Setup for a dog shelter object in the database"""
    __tablename__ = "shelter"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(50))
    zip_code = Column(String(10))
    website = Column(String(100))

class Puppy(Base):
    """Setup for a puppy object to store in the database"""
    __tablename__ = "puppy"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    picture = Column(String)
    breed = Column(String(50))
    gender = Column(String(6), nullable=False)
    weight = Column(Numeric(10))

    shelter_id = Column(Integer, ForeignKey("shelter.id"))
    shelter = relationship(Shelter)


engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
