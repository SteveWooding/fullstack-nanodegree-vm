#!/usr/bin/env python
"""Check in a puppy into a shelter.

Checks to see if the requested shelter is full and asks
the user for an alterative. If all the shelters are full,
inform the user to open a new shelter.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy

def check_in_puppy(db_session, puppy, shelter_id):
    """Check a puppy into a shelter.

    Make sure the shelter has room. Prompt the user to try a different shelter
    if their first choice is full.

    Args:
        db_session: SQLalchemy database session object
        puppy (Puppy): Puppy instance to add to a shelter
        shelter_id (int): ID of the requested shelter to add puppy to
    """
    shelter = db_session.query(Shelter).filter_by(id=shelter_id).one()

    if shelter.current_occupancy == shelter.max_capacity:
        print "That shelter is full!"
        num_shelters = db_session.query(Shelter).count()
        full_shelters = [shelter_id]
        found_free_shelter = False

        while found_free_shelter is False:
            if len(full_shelters) == num_shelters:
                print "All shelters are full. A new one needs to be opened."
                return
            shelter_id = input("Enter another shelter ID number to try: ")
            shelter = db_session.query(Shelter).filter_by(id=shelter_id).one()

            if shelter.current_occupancy == shelter.max_capacity:
                print "That shelter is also full!"
                full_shelters.append(shelter_id)
                continue
            else:
                found_free_shelter = True

    puppy.shelter_id = shelter_id
    shelter.current_occupancy += 1
    db_session.add(puppy)
    db_session.add(shelter)
    db_session.commit()


if __name__ == "__main__":
    # Setup the connection to the database
    engine = create_engine("sqlite:///puppyshelter.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Create a new puppy and check it into a shelter given by the user.
    new_puppy = Puppy(name="Fred", gender="male")
    req_shelter_id = input("Enter a shelter ID to check the puppy into: ")
    check_in_puppy(session, new_puppy, req_shelter_id)
