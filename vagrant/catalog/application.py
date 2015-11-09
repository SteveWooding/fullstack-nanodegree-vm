#!/usr/bin/env python
import os.path

from database_setup import Base, User, Category, Item, create_db
from populate_database import populate_database

if __name__ == '__main__':
    if os.path.isfile('itemcatalog.db') is False:
        create_db()
        populate_database()
