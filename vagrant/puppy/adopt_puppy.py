#!/usr/bin/env python
"""Function to adopt a puppy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Puppy, Adopter, Shelter

def adopt_puppy(db_session, puppy_id, adopter_ids):
    """Let people adopt a puppy.

    Args:
        puppy_id (int): ID for the puppy to be adopted
        adopter_ids (list): List of adopter IDs.
    """
    puppy = db_session.query(Puppy).filter_by(id=puppy_id).one()

    if puppy.shelter_id is not None:
        puppy.adopters = adopter_ids
        shelter = db_session.query(Shelter).filter_by(id=puppy.shelter_id).one()
        shelter.current_occupancy -= 1
        puppy.shelter_id = None

        db_session.add(puppy)
        db_session.add(shelter)
        db_session.commit()
    else:
        print "Error: Puppy is not currently in a shelter, so can't be adopted."


if __name__ == "__main__":
    # Setup the connection to the database
    engine = create_engine("sqlite:///puppyshelter.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Create a couple of adopters.
    new_adopter_1 = Adopter(name="Alice")
    new_adopter_2 = Adopter(name="Bob")

    session.add(new_adopter_1)
    session.add(new_adopter_2)
    session.commit()

    adopter_1_id = session.query(Adopter).filter_by(name="Alice").first()
    adopter_2_id = session.query(Adopter).filter_by(name="Bob").first()

    adopt_puppy(session, 2, [adopter_1_id, adopter_2_id])

    # Check the status of puppy 1.
    adopted_puppy = session.query(Puppy).filter_by(id=1).one()
    print(adopted_puppy.shelter_id, adopted_puppy.adopters[0].name,
          adopted_puppy.adopters[1].name)
