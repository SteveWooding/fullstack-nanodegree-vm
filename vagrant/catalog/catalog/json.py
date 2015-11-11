"""Defines JSON API endpoints."""
from flask import jsonify

from catalog import app, session

@app.route('/catalog.json/')
def items_json():
    """Returns all the items in the catalog as a JSON file."""
    return "Test"
