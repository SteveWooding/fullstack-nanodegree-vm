from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Make an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "No restaurant exists with that ID."

    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        session.add(edited_item)
        session.commit()
        flash("menu item has been edited!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=edited_item)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash("menu item has been deleted!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html',
                               restaurant_id=restaurant_id,
                               item=item_to_delete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
