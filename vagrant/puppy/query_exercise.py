#!/usr/bin/env python
"""Perform queries of the database to complete excercise"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
import datetime
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
date_6_months_ago = datetime.date.today() - datetime.timedelta(days=182)
young_puppies = (session.query(Puppy).
                 filter(Puppy.date_of_birth > date_6_months_ago).
                 order_by(desc(Puppy.date_of_birth)).
                 all())
print
for puppy in young_puppies:
    print puppy.name, puppy.date_of_birth


# 3. Query all puppies by ascending weight.
puppies = session.query(Puppy).order_by(Puppy.weight).all()
print
for puppy in puppies:
    print puppy.name, puppy.weight


# 4. Query all puppies grouped by the shelter in which they are staying.
puppies_by_shelter = (session.query(Puppy).
                      order_by(Puppy.shelter_id).
                      all())
print
for puppy in puppies_by_shelter:
    print puppy.name, puppy.shelter.name
