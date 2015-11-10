"""Defines the views to be presented to the user."""
from flask import render_template

from catalog import app

# Dummy database for testing the templates
categories = [
    {'id': '1', 'name': 'Mammals'},
    {'id': '2', 'name': 'Birds'},
    {'id': '3', 'name': 'Fish'},
    {'id': '4', 'name': 'Reptiles'},
    {'id': '5', 'name': 'Amphibians'},
    {'id': '6', 'name': 'Arthropods'},
]

category = {'id': '1', 'name': 'Mammals'}

items = [
    {'id': '1', 'name': 'Elephant', 'description': 'Large, grey animal',
     'category_id': '1'},
    {'id': '2', 'name': 'Polar Bear', 'description': 'Large, white animal',
     'category_id': '1'},
    {'id': '3', 'name': 'Kingfisher', 'description': 'Bird that eats fish',
     'category_id': '2'},
    {'id': '4', 'name': 'Blue Tit', 'description': 'A blue & yellow bird',
     'category_id': '2'},
    {'id': '5', 'name': 'Swordfish', 'description': 'Fish with a sword',
     'category_id': '3'},
    {'id': '6', 'name': 'Whale Shark', 'description': 'A big shark',
     'category_id': '3'}
]

item = {'id': '1', 'name': 'Elephant', 'description': 'Large, grey animal',
        'category_id': '1'}

@app.route('/')
@app.route('/catalog/')
def show_homepage():
    """Show the homepage diplaying the categories and latest items."""
    return render_template('homepage.html',
                           categories=categories,
                           latest_items=items)


@app.route('/catalog/<category_name>/items/')
def show_items(category_name):
    """Show items belonging to a specified category."""
    return render_template('items.html',
                           categories=categories,
                           category=category,
                           items=items)


@app.route('/catalog/<category_name>/<item_name>/')
def show_item(category_name, item_name):
    """Show details of a particular item belonging to a specified category."""
    return render_template('item.html',
                           categories=categories,
                           category=category,
                           item=item)


@app.route('/catalog/new/')
def create_item():
    """Allow users to create a new item in the catalog."""
    return render_template('new_item.html',
                           categories=categories)


@app.route('/catalog/<item_name>/edit/')
def edit_item(item_name):
    """Edit the details of the specified item."""
    return render_template('edit_item.html',
                           categories=categories,
                           item=item)


@app.route('/catalog/<item_name>/delete/')
def delete_item(item_name):
    """Delete a specified item from the database."""
    return "Delete the %s item." % item_name
