# This is where our imports go.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flaskr import config
from flask_googlemaps import GoogleMaps
from flaskr import key

# These are the configurations we need for flask and SQLite
app = Flask(__name__)
app.config.from_object(config.Config)
app.config['GOOGLEMAPS_KEY'] = key
db = SQLAlchemy(app)
db.init_app(app)

# you can also pass the key here if you prefer


# Create all database tables
engine = create_engine('sqlite:///cases.db', echo = True)

from flaskr import routes