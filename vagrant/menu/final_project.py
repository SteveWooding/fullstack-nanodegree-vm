from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Fake Restaurants (just to test page layout)
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'},
               {'name':'Blue Burgers', 'id':'2'},
               {'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items (just to test page layout)
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'id':'1', 'restaurant_id':'1'}


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
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('new_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """Edit a restaurant"""
    restaurant_to_edit = (session.query(Restaurant).
                          filter_by(id=restaurant_id).one())
    if request.method == 'POST':
        if request.form['name']:
            restaurant_to_edit.name = request.form['name']
        session.add(restaurant_to_edit)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('edit_restaurant.html',
                               restaurant=restaurant_to_edit)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """Delete a restaurant"""
    restaurant_to_delete = (session.query(Restaurant).
                            filter_by(id=restaurant_id).one())
    if request.method == 'POST':
        session.delete(restaurant_to_delete)
        session.commit()
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
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
    """Edit a menu item"""
    return render_template('edit_menu_item.html',
                           restaurant=restaurant,
                           item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
    """Delete a menu item"""
    return render_template('delete_menu_item.html',
                           restaurant=restaurant,
                           item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)