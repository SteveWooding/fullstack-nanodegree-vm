"""Provides an XML API endpoint."""
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from catalog import app
from database_setup import Category, Item
from connect_to_database import connect_to_database

@app.route('/catalog.xml/')
def items_xml():
    """Returns all the items as an XML file.

    Research for this function came from:
        https://pymotw.com/2/xml/etree/ElementTree/create.html
    """
    session = connect_to_database()
    categories = session.query(Category).all()

    root = Element('catalog')

    for category in categories:
        cat_tag = SubElement(root,
                             'category',
                             {'id':str(category.id), 'name':category.name})

        items = session.query(Item).filter_by(category=category).all()

        for item in items:
            item_tag = SubElement(cat_tag, 'item', {'id':str(item.id)})
            name_tag = SubElement(item_tag, 'name')
            name_tag.text = item.name
            desc_tag = SubElement(item_tag, 'description')
            desc_tag.text = item.description

    session.close()

    # Return the XML with a 2 space indent to make it more human readable.
    return parseString(tostring(root, 'utf-8')).toprettyxml(indent='  ')