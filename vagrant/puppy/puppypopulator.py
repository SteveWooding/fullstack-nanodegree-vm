#!/usr/bin/env python
"""Populate the puppy shelter database with entries."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy, Profile
from random import randint
import datetime
import random


# Setup the connection to the database
engine = create_engine("sqlite:///puppyshelter.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add Shelters
shelter1 = Shelter(name="Oakland Animal Services",
                   address="1101 29th Ave",
                   city="Oakland",
                   state="California",
                   zip_code="94601",
                   website="oaklandanimalservices.org",
                   max_capacity=34)
session.add(shelter1)

shelter2 = Shelter(name="San Francisco SPCA Mission Adoption Center",
                   address="250 Florida St",
                   city="San Francisco",
                   state="California",
                   zip_code="94103",
                   website="sfspca.org",
                   max_capacity=25)
session.add(shelter2)

shelter3 = Shelter(name="Wonder Dog Rescue",
                   address="2926 16th Street",
                   city="San Francisco",
                   state="California",
                   zip_code="94103",
                   website="http://wonderdogrescue.org",
                   max_capacity=33)
session.add(shelter3)

shelter4 = Shelter(name="Humane Society of Alameda",
                   address="PO Box 1571",
                   city="Alameda",
                   state="California",
                   zip_code="94501",
                   website="hsalameda.org",
                   max_capacity=42)
session.add(shelter4)

shelter5 = Shelter(name="Palo Alto Humane Society",
                   address="1149 Chestnut St.",
                   city="Menlo Park",
                   state="California",
                   zip_code="94025",
                   website="paloaltohumane.org",
                   max_capacity=10)
session.add(shelter5)

session.commit()

# Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy", "Rocky", "Jake", "Jack",
              "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley",
              "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar",
              "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo",
              "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus",
              "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco",
              "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo",
              "Boomer", "Luke", "Henry"]

female_names = ["Bella", "Lucy", "Molly", "Daisy", "Maggie", "Sophie", "Sadie",
                "Chloe", "Bailey", "Lola", "Zoe", "Abby", "Ginger", "Roxy",
                "Gracie", "Coco", "Sasha", "Lily", "Angel", "Princess", "Emma",
                "Annie", "Rosie", "Ruby", "Lady", "Missy", "Lilly", "Mia",
                "Katie", "Zoey", "Madison", "Stella", "Penny", "Belle", "Casey",
                "Samantha", "Holly", "Lexi", "Lulu", "Brandy", "Jasmine",
                "Shelby", "Sandy", "Roxie", "Pepper", "Heidi", "Luna", "Dixie",
                "Honey", "Dakota"]

puppy_images = [
    "http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct",
    "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct",
    "http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct",
    "http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct",
    "http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg",
    "http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct",
    "http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct",
    "http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct",
    "http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct",
    "http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

puppy_descriptions = ["So cute", "Very well behaved", "Adorable",
                      "Little bundle of joy"]

def CreateRandomAge():
    """Create a random age for a puppy.

    This method will make a random age for each puppy between 0-18 months
    (approx.) old from the day the algorithm was run.

    Returns:
        birthday(date): Date the puppy was born.
    """
    today = datetime.date.today()
    days_old = randint(0, 540)
    birthday = today - datetime.timedelta(days=days_old)
    return birthday

# This method will create a random weight between 1.0-40.0 pounds (or whatever
# unit of measure you prefer)
def CreateRandomWeight():
    """Create a random weight for a puppy.

    This method will create a random weight between 1.0-40.0 pounds (or whatever
    unit of measure you prefer).

    Returns:
        float: Random weight of puppy.
    """
    return random.uniform(1.0, 40.0)


for i, male_name in enumerate(male_names):
    new_puppy = Puppy(name=male_name,
                      gender="male",
                      date_of_birth=CreateRandomAge(),
                      shelter_id=randint(1, 5),
                      weight=CreateRandomWeight())

    new_profile = Profile(description=random.choice(puppy_descriptions),
                          picture=random.choice(puppy_images),
                          puppy_id=i + 1)

    shelter = session.query(Shelter).filter_by(id=new_puppy.shelter_id).one()
    if shelter.current_occupancy == shelter.max_capacity:
        # Find shelter with some room
        free_shelter = (session.query(Shelter).
                         filter(Shelter.current_occupancy < Shelter.max_capacity).first())
        new_puppy.shelter_id = free_shelter.id
        free_shelter.current_occupancy += 1
        session.add(free_shelter)
    else:
        shelter.current_occupancy += 1
        session.add(shelter)

    session.add(new_puppy)
    session.add(new_profile)
    session.commit()

num_males = len(male_names)

for i, female_name in enumerate(female_names):
    new_puppy = Puppy(name=female_name,
                      gender="female",
                      date_of_birth=CreateRandomAge(),
                      shelter_id=randint(1, 5),
                      weight=CreateRandomWeight())

    new_profile = Profile(description=random.choice(puppy_descriptions),
                          picture=random.choice(puppy_images),
                          puppy_id=i + num_males + 1)

    shelter = session.query(Shelter).filter_by(id=new_puppy.shelter_id).one()
    if shelter.current_occupancy == shelter.max_capacity:
        # Find shelter with some room
        free_shelter = (session.query(Shelter).
                         filter(Shelter.current_occupancy < Shelter.max_capacity).first())
        new_puppy.shelter_id = free_shelter.id
        free_shelter.current_occupancy += 1
        session.add(free_shelter)
    else:
        shelter.current_occupancy += 1
        session.add(shelter)

    session.add(new_puppy)
    session.add(new_profile)
    session.commit()
