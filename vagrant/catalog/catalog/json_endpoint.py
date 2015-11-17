"""Defines JSON API endpoints."""
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from database_setup import Category, Item
from connect_to_database import connect_to_database

@app.route('/catalog.json/')
def items_json():
    """Returns all the items in the catalog as a JSON file.

    The for loop in the call to jsonify() goes through each category and,
    because the Category class has a reference to the items in it, for each
    item a call to its serialise function is made. So we end up with a JSON
    array of items for each category.
    """
    session = connect_to_database()
    categories = session.query(Category).all()
    serialised_catergories = [i.serialise for i in categories]
    session.close()
    return jsonify(Category=serialised_catergories)


@app.route('/catalog/<category_name>/<item_name>/JSON/')
@app.route('/catalog/<item_name>/JSON/')
def item_json(item_name, category_name=None):
    """Returns a single item in a JSON file."""
    session = connect_to_database()
    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        # TODO Make this a flash message on homepage.
        session.close()
        return "The item '%s' does not exist." % item_name

    session.close()
    return jsonify(Item=item.serialise)
