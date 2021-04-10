# This is where our imports go.
from flask import Flask
import os

# These are the configurations we need for flask and SQLite
app = Flask(__name__)

from flaskr import routes