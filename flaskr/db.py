'''
Maintainer: Timothy Player
Date: Mar. 18th 2021
Description: This hosts the logic for our database. We need to hold blobs which are jsons
containing user hashes, where they were and at what date they were there. 
WE DO NOT HOLD ANY PERSONAL INFORMATION!!!! i.e. name/birthdate/sex... to 
identify someone we are not a dev team.
'''
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class locations(db.Model):
    """Stores locations."""
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)


class case(db.Model):
    """Stores the location & time"""
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'))

    longitude = db.Column(db.Integer)
    latitude = db.Column(db.Integer)
    time = db.Column(db.String(30))

    # Relationship
    locations = db.relationship(
        'locations',
        backref=db.backref('case', lazy='dynamic', collection_class=list)
    )