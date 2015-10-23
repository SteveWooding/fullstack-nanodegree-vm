#!/usr/bin/env python
"""Perform queries testing different associations"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, Profile

# Setup the connection to the database
engine = create_engine("sqlite:///puppyshelter.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Print out the puppy name and description, which is held in the profile table
puppies = session.query(Puppy).all()
for puppy in puppies:
    print puppy.name, puppy.profile.description
