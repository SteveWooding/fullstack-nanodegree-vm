"""Initialisation for the catalog package."""
from flask import Flask
app = Flask(__name__)

import catalog.views
