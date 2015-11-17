"""Initialisation for the catalog package."""
from flask import Flask
from flask.ext.seasurf import SeaSurf

from catalog.database_setup import Base


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

app = Flask(__name__)

# SeaSurf anti-CSRF Flask extension
csrf = SeaSurf(app)


# OK to have circular imports here as they are not used in this file.
# Ref: http://flask.pocoo.org/docs/0.10/patterns/packages/
import catalog.views
import catalog.json_endpoint
import catalog.xml_generator
import catalog.auth
