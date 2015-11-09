#!/usr/bin/env python
import os.path

from catalog import app
from catalog.database_setup import create_db
from catalog.populate_database import populate_database

if __name__ == '__main__':
    if os.path.isfile('itemcatalog.db') is False:
        create_db()
        populate_database()

    app.debug = True
    app.run(host='0.0.0.0', port=8000)