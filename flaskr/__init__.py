# This is where our imports go.
from alembic.config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_googlemaps import GoogleMaps

# make key.py with API_KEY='your_api_string'
from flaskr import config, key

alembic_cfg = Config()

# These are the configurations we need for flask and SQLite
app = Flask(__name__)
app.config.from_object(config.Config)
app.config["GOOGLEMAPS_KEY"] = key.API_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:webapp@host.docker.internal:5432/asymptomatix"

db = SQLAlchemy(app)
db.init_app(app)

# you can also pass the key here if you prefer


# Create all database tables
engine = create_engine("sqlite:///cases.db", echo=True)
migrate = Migrate(app, db, include_schemas=True)

from flaskr import routes
