"""Connect to the database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog import app
from catalog.database_setup import Base

def connect_to_database():
    """Connects to the database and returns an sqlalchemy session object."""
    engine = create_engine(app.config['DATABASE_URL'])
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()

    return session
