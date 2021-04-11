# This is where our imports go.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os

# These are the configurations we need for flask and SQLite
app = Flask(__name__)
app.config['SECRET_KEY'] = 'IHADLF@#)%#*@#PHKANDLI82123'
db = SQLAlchemy(app)
engine = create_engine('sqlite:///cases.db', echo = True)

from flaskr import routes, database