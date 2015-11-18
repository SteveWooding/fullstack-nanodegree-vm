"""Defines the views to be presented to the user."""
import os
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flask import session as login_session
from werkzeug import secure_filename
from sqlalchemy import desc, literal
from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from catalog.database_setup import Category, Item
from catalog.connect_to_database import connect_to_database


def allowed_file(filename):
    """Check if the filename has one of the allowed extensions."""
    return ('.' in filename and filename.rsplit('.', 1)[1] in
            app.config['ALLOWED_EXTENSIONS'])


def delete_image(filename):
    """Delete an item image file from the filesystem."""
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except OSError:
        print "Error deleting image file %s" % filename


@app.route('/')
@app.route('/catalog/')
def show_homepage():
    """Show the homepage diplaying the categories and latest items."""
    session = connect_to_database()
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by(desc(Item.id))[0:10]
    session.close()
    return render_template('homepage.html',
                           categories=categories,
                           latest_items=latest_items)


@app.route('/catalog/<category_name>/items/')
def show_items(category_name):
    """Show items belonging to a specified category."""
    session = connect_to_database()
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % category_name)
        return redirect(url_for('show_homepage'))

    categories = session.query(Category).all()
    items = (session.query(Item).filter_by(category=category).
             order_by(Item.name).all())
    session.close()
    return render_template('items.html',
                           categories=categories,
                           category=category,
                           items=items)


@app.route('/catalog/<category_name>/<item_name>/')
def show_item(category_name, item_name):
    """Show details of a particular item belonging to a specified category."""
    session = connect_to_database()
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % category_name)
        session.close()
        return redirect(url_for('show_homepage'))

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("The item '%s' does not exist." % item_name)
        session.close()
        return redirect(url_for('show_items', category_name=category_name))

    categories = session.query(Category).all()
    session.close()
    return render_template('item.html',
                           categories=categories,
                           category=category,
                           item=item)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def create_item():
    """Allow users to create a new item in the catalog."""
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_to_database()

    if request.method == 'POST':
        if not request.form['name']:
            flash("New animal not created: No name provided.")
            return redirect(url_for('show_homepage'))

        if request.form['name'] == "items":
            # Can't have an item called "items" as this is a route.
            flash("Error: Can't have an animal called 'items'.")
            return redirect(url_for('show_homepage'))

        # Enforce rule that item names are unique
        qry = session.query(Item).filter(Item.name == request.form['name'])
        already_exists = (session.query(literal(True)).
                          filter(qry.exists()).scalar())
        if already_exists is True:
            flash("Error: There is already an animal with the name '%s'"
                  % request.form['name'])
            session.close()
            return redirect(url_for('show_homepage'))

        category = (session.query(Category)
                    .filter_by(name=request.form['category']).one())
        new_item = Item(category=category,
                        name=request.form['name'],
                        description=request.form['description'],
                        quantity=request.form['quantity'],
                        user_id=login_session['user_id'])

        # Process optional item image
        image_file = request.files['file']
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            if os.path.isdir(app.config['UPLOAD_FOLDER']) is False:
                os.mkdir(app.config['UPLOAD_FOLDER'])
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_item.image_filename = filename

        elif request.form['image_url']:
            new_item.image_url = request.form['image_url']

        session.add(new_item)
        session.commit()

        flash("New animal successfully created!")
        category_name = category.name
        item_name = new_item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))
    else:
        categories = session.query(Category).all()

        # See, if any, which category page new item was click on.
        ref_category = None
        if 'catalog' in request.referrer:
            ref_url_elements = request.referrer.split('/')
            if len(ref_url_elements) > 5:
                ref_category = ref_url_elements[4]

        session.close()
        return render_template('new_item.html',
                               categories=categories,
                               ref_category=ref_category)


@app.route('/catalog/<item_name>/edit/', methods=['GET', 'POST'])
def edit_item(item_name):
    """Edit the details of the specified item."""
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_to_database()

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_name)
        return redirect(url_for('show_homepage'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't add this animal, so you can't edit it. Sorry :-(")
        category = session.query(Category).filter_by(id=item.category_id).one()
        session.close()
        return redirect(url_for('show_item',
                                category_name=category.name,
                                item_name=item.name))

    if request.method == 'POST':
        if request.form['name'] != item.name:
            # Enforce rule that item names are unique
            qry = session.query(Item).filter(Item.name == request.form['name'])
            already_exists = (session.query(literal(True)).filter(qry.exists())
                              .scalar())
            if already_exists is True:
                original_category = (session.query(Category)
                                     .filter_by(id=item.category_id).one())
                flash("Error: There is already an animal with the name '%s'"
                      % request.form['name'])
                session.close()
                return redirect(url_for('show_items',
                                        category_name=original_category.name))
            item.name = request.form['name']

        form_category = (session.query(Category)
                         .filter_by(name=request.form['category']).one())
        if form_category != item.category:
            item.category = form_category

        item.description = request.form['description']
        item.quantity = request.form['quantity']

        # Process optional item image
        image_file = request.files['file']
        if image_file and allowed_file(image_file.filename):
            if item.image_filename:
                delete_image(item.image_filename)
            filename = secure_filename(image_file.filename)
            if os.path.isdir(app.config['UPLOAD_FOLDER']) is False:
                os.mkdir(app.config['UPLOAD_FOLDER'])
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            item.image_filename = filename
            item.image_url = None

        elif ('delete_image' in request.form and
              request.form['delete_image'] == 'delete'):
            if item.image_filename:
                delete_image(item.image_filename)
                item.image_filename = None

        if not image_file and request.form['image_url']:
            item.image_url = request.form['image_url']
            if item.image_filename:
                delete_image(item.image_filename)
                item.image_filename = None

        session.add(item)
        session.commit()

        flash("Animal successfully edited!")
        category_name = form_category.name
        item_name = item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))
    else:
        categories = session.query(Category).all()
        session.close()
        return render_template('edit_item.html',
                               categories=categories,
                               item=item)


@app.route('/catalog/<item_name>/delete/', methods=['GET', 'POST'])
def delete_item(item_name):
    """Delete a specified item from the database."""
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_to_database()

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_name)
        session.close()
        return redirect(url_for('show_homepage'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't add this animal, so you can't delete it. Sorry :-(")
        category = session.query(Category).filter_by(id=item.category_id).one()
        category_name = category.name
        item_name = item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))

    if request.method == 'POST':
        if item.image_filename:
            delete_image(item.image_filename)
        session.delete(item)
        session.commit()
        category = session.query(Category).filter_by(id=item.category_id).one()

        flash("Animal successfully deleted!")
        category_name = category.name
        session.close()
        return redirect(url_for('show_items', category_name=category_name))
    else:
        categories = session.query(Category).all()
        session.close()
        return render_template('delete_item.html',
                               categories=categories,
                               item=item)


@app.route('/item_images/<filename>')
def show_item_image(filename):
    """Route to serve user uploaded images."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
