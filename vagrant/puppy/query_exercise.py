#!/usr/bin/env python
"""Perform queries of the database to complete excercise"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy

# Setup the connection to the database
engine = create_engine("sqlite:///puppyshelter.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# 1. Query all of the puppies and return the results in ascending alphabetical
#    order.
puppies = session.query(Puppy).order_by(Puppy.name).all()
for puppy in puppies:
    print puppy.name


# 2. Query all of the puppies that are less than 6 months old organized by the
#    youngest first.



# 3. Query all puppies by ascending weight.



# 4. Query all puppies grouped by the shelter in which they are staying.
