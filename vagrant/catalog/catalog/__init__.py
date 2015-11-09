#!/usr/bin/env python
import os.path

from flask import Flask

from database_setup import Base, User, Category, Item, create_db
from populate_database import populate_database

app = Flask(__name__)

@app.route('/')
@app.route('/catalog/')
def show_homepage():
    """Show the homepage diplaying the categories and latest items."""
    return "Homepage"


@app.route('/catalog/<category_name>/items')
def show_items(category_name):
    """Show items belonging to a specified category."""
    return "Items belonging to the %s category." % category_name


@app.route('/catalog/<category_name>/<item_name>')
def show_item(category_name, item_name):
    """Show details of a particular item belonging to a specified category."""
    return "Show details of item %s in category %s." % (item_name, category_name)


@app.route('/catalog/<item_name>/edit')
def edit_item(item_name):
    """Edit the details of the specified item."""
    return "Edit details of the %s item." % item_name


@app.route('/catalog/<item_name>/delete')
def delete_item(item_name):
    """Delete a specified item from the database."""
    return "Delete the %s item." % item_name


if __name__ == '__main__':
    if os.path.isfile('itemcatalog.db') is False:
        create_db()
        populate_database()

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
