# This is where our imports go.
from flask import Flask
from flaskr import db
from flaskr import geoform
import os

# These are the configurations we need for flask and SQLite
app = Flask(__name__)
app.config['SECRET_KEY'] = 'IHADLF@#)%#*@#PHKANDLI82123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cases.db'
db.init_app(app)
db.create_all(app=app)

from flaskr import routes