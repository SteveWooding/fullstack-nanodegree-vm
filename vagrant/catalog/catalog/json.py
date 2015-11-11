"""Defines JSON API endpoints."""
from flask import jsonify

from catalog import app, session
from database_setup import Category

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
