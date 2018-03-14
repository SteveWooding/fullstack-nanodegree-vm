"""Allows users to login to the web app via outh providers."""
import random, string
from flask import render_template, request, redirect, url_for, flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import session as login_session
from sqlalchemy.orm.exc import NoResultFound
import httplib2
import json
from flask import make_response
import requests

from catalog import app
from catalog.database_setup import User, Category
from catalog.connect_to_database import connect_to_database


@app.route('/login')
def show_login():
    """Show the login screen to the user."""
    # Create a state token to prevent request forgery.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    session = connect_to_database()
    categories = session.query(Category).all()
    session.close()

    return render_template('login.html', STATE=state, categories=categories)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Performs app login via Google oauth."""
    g_client_secrets_file = (app.config['OAUTH_SECRETS_LOCATION'] +
                             'g_client_secrets.json')
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization one-time code into a credentials object
        oauth_flow = flow_from_clientsecrets(g_client_secrets_file, scope='')
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
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

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
    g_client_id = json.loads(
        open(g_client_secrets_file, 'r').read())['web']['client_id']
    if result['issued_to'] != g_client_id:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's."), 401)
        print "Token's client ID doesn't match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
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

    # Check if the user exists in the database. If not create a new user.
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        user_id = create_user()
    login_session['user_id'] = user_id

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


def gdisconnect():
    """Revoke a current user's token and reset their login session."""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Login via Facebook OAuth"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data

    # Exchange client token for long-lived server-side token
    fb_client_secrets_file = (app.config['OAUTH_SECRETS_LOCATION'] +
                              'fb_client_secrets.json')
    app_id = json.loads(
        open(fb_client_secrets_file, 'r').read())['web']['app_id']
    app_secret = json.loads(
        open(fb_client_secrets_file, 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/v2.12/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    # Extract the access token from response
    token = 'access_token=' + data['access_token']

    # Use token to get user info from API.
    url = 'https://graph.facebook.com/v2.12/me?%s&fields=name,id,email' % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to proplerly
    # logout, let's strip out the information before the equals sign in
    # our token.
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = ('https://graph.facebook.com/v2.12/me/picture?%s&redirect=0'
           '&height=200&width=200') % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # Check if the user exists in the database. If not create a new user.
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        user_id = create_user()
    login_session['user_id'] = user_id

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


def fbdisconnect():
    """Logout via Facebook OAuth."""
    facebook_id = login_session['facebook_id']

    # The access token must be included to successfully logout.
    access_token = login_session['access_token']

    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s') % (facebook_id, access_token)

    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]

    if result == '{"success":true}':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    """Generic logout function that supports multiple OAuth providers."""
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']

        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        flash("You have successfully been logged out.")
        return redirect(url_for('show_homepage'))

    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('show_homepage'))


def create_user():
    """Create a new user in the database."""
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session = connect_to_database()
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    session.close()
    return user.id


def get_user_id(email):
    """Given an email address, return the user ID, if in the database.

    Args:
        email (str): The email address associated with the user account.

    Returns:
        The user id number stored in the database.
    """
    session = connect_to_database()
    try:
        user = session.query(User).filter_by(email=email).one()
        session.close()
        return user.id
    except NoResultFound:
        session.close()
        return None
