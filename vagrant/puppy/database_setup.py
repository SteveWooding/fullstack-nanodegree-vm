#!/usr/bin/env python
"""Setup a database of puppies and dog shelters"""
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
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
    max_capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer)


association_table = Table(
    "association", Base.metadata,
    Column("puppy_id", Integer, ForeignKey("puppy.id")),
    Column("adopter_id", Integer, ForeignKey("adopter.id")))


class Puppy(Base):
    """Setup for a puppy object to store in the database"""
    __tablename__ = "puppy"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    breed = Column(String(50))
    gender = Column(String(6), nullable=False)
    weight = Column(Numeric(10))

    shelter_id = Column(Integer, ForeignKey("shelter.id"))
    shelter = relationship(Shelter)

    # Each puppy has one profile containing extra info.
    # This is a one-to-one association.
    profile = relationship("Profile", uselist=False, backref="puppy")

    # Each puppy can have one or more adopters.
    # This is a many-to-many association.
    adopters = relationship("Adopter",
                            secondary=association_table,
                            backref="puppies")


class Profile(Base):
    """Setup for a puppy profile object.

    One puppy may only have one profile.
    """
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String, nullable=False)
    special_needs = Column(String)

    puppy_id = Column(Integer, ForeignKey("puppy.id"))


class Adopter(Base):
    """Setup for an adopter object and table.

    A puppy may be adopted by more than one person, or one person may adopt
    many puppies, so this is a many-to-many relationship.
    """
    __tablename__ = "adopter"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
