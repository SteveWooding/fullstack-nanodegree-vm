from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    """Show all restaurants"""
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def new_restaurant():
    """Create a new restaurant"""
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('new_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """Edit a restaurant"""
    try:
        restaurant_to_edit = (session.query(Restaurant).
                              filter_by(id=restaurant_id).one())
    except:
        return "No restaurant exists with that ID."
    if request.method == 'POST':
        if request.form['name']:
            restaurant_to_edit.name = request.form['name']
        session.add(restaurant_to_edit)
        session.commit()
        flash("Restaurant Successfully Edited")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('edit_restaurant.html',
                               restaurant=restaurant_to_edit)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """Delete a restaurant"""
    try:
        restaurant_to_delete = (session.query(Restaurant).
                                filter_by(id=restaurant_id).one())
    except NoResultFound:
        return "No restaurant exists with that ID."
    if request.method == 'POST':
        session.delete(restaurant_to_delete)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('delete_restaurant.html',
                               restaurant=restaurant_to_delete)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    """Show a restaurant menu"""
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "No restaurant exists with that ID." # Could create an error page
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def new_menu_item(restaurant_id):
    """Create a new menu item"""
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "No restaurant exists with that ID." # Could create an error page
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            course=request.form['course'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New Menu Item Created")
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET','POST'])
def edit_menu_item(restaurant_id, menu_id):
    """Edit a menu item"""
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "No restaurant exists with that ID." # Could create an error page
    try:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
    except NoResultFound:
        return "No menu item exists with that ID."
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        if request.form['course']:
            item.course = request.form['course']
        session.add(item)
        session.commit()
        flash("Menu Item Successfully Edited")
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html',
                               restaurant=restaurant,
                               item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET','POST'])
def delete_menu_item(restaurant_id, menu_id):
    """Delete a menu item"""
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "No restaurant exists with that ID." # Could create an error page
    try:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
    except NoResultFound:
        return "No menu item exists with that ID."
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu Item Successfully Deleted")
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html',
                               restaurant=restaurant,
                               item=item)


# Make JSON API endpoints for restaurants and menu items
@app.route('/restaurants/JSON/')
def restaurants_json():
    """Returns a JSON file containing the restaurants."""
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurant_menu_json(restaurant_id):
    """Returns a JSON file of menu items for a restaurant."""
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except:
        return "No restaurant exists with that ID."
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurant_menu_item_json(restaurant_id, menu_id):
    """Returns a JSON file of a single menu item."""
    try:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
    except:
        return "No menu item exists with that ID."
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # This needs changing if production
    app.debug = True
    app.run(host='0.0.0.0', port=5000)