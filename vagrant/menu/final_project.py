from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

# Imports for login feature
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json',  'r').read())['web']['client_id']

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@app.route('/login')
def show_login():
    """Show the login screen to a user."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Performs app login via Google oauth."""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization one-time code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's."), 401)
        print "Token's client ID doesn't match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in.
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the acces token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


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