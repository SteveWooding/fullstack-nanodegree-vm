#!/usr/bin/env python
"""Perform queries testing different associations"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, Profile, Adopter

# Setup the connection to the database
engine = create_engine("sqlite:///puppyshelter.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Print out the puppy name and description, which is held in the profile table
puppies = session.query(Puppy).all()
for puppy in puppies:
    print puppy.name, puppy.profile.description
print

# Have Jack and Jill adopt the puppy Max, first checking to see if this has
# been run before on the database.
qry = session.query(Adopter).filter_by(name="Jack")
jack_exists = session.query(qry.exists())
qry = session.query(Adopter).filter_by(name="Jill")
jill_exists = session.query(qry.exists())
if jack_exists is False and jill_exists is False:
    puppy = session.query(Puppy).filter_by(name="Max").one()
    puppy.adopters = [Adopter(name="Jack"), Adopter(name="Jill")]
    session.add(puppy)
    session.commit()
else:
    print "Already had Max adopted by Jack and Jill before."

# Check to see that Jack and Jill have adopted Max
adopters = session.query(Adopter).all()
for adopter in adopters:
    print adopter.name, adopter.puppies[0].name
