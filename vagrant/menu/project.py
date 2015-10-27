from flask import Flask
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
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "No restaurant exists with that ID."

    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    for item in items:
        output += '<p>'
        output += item.name
        output += '</br>'
        output += item.price
        output += '</br>'
        output += item.description
        output += '</p>'

    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
