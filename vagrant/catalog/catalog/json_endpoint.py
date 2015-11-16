"""Defines JSON API endpoints."""
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from catalog import app, session
from database_setup import Category, Item

@app.route('/catalog.json/')
def items_json():
    """Returns all the items in the catalog as a JSON file.

    The for loop in the call to jsonify() goes through each category and,
    because the Category class has a reference to the items in it, for each
    item a call to its serialise function is made. So we end up with a JSON
    array of items for each category.
    """
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialise for i in categories])


@app.route('/catalog/<category_name>/<item_name>/JSON/')
@app.route('/catalog/<item_name>/JSON/')
def item_json(item_name, category_name=None):
    """Returns a single item in a JSON file."""
    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        # TODO Make this a flash message on homepage.
        return "The item '%s' does not exist." % item_name

    return jsonify(Item=item.serialise)
