from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    """Show all restaurants"""
    return "This page will show all my restaurants"


@app.route('/restaurant/new/')
def new_restaurant():
    """Create a new restaurant"""
    return "This page will be for making a new restaurant"


@app.route('/restaurant/<int:restaurant_id>/edit/')
def edit_restaurant(restaurant_id):
    """Edit a restaurant"""
    return "This page will be for editing restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/')
def delete_restaurant(restaurant_id):
    """Delete a restaurant"""
    return "This page will be for deleting restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    """Show a restaurant menu"""
    return "This page is the menu for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def new_menu_item(restaurant_id):
    """Create a new menu item"""
    return "This page is for making a new menu item for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
    """Edit a menu item"""
    return "This page is for editing menu item %s" % menu_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
    """Delete a menu item"""
    return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)