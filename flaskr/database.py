'''
Maintainer: Timothy Player
Date: Mar. 18th 2021
Description: This hosts the logic for our database. We need to hold blobs which are jsons
containing user hashes, where they were and at what date they were there. 
WE DO NOT HOLD ANY PERSONAL INFORMATION!!!! i.e. name/birthdate/sex... to 
identify someone we are not a dev team.
'''
from flaskr import db

class Person(db.Model):
    """Stores locations of this person."""
    __tablename__ = 'People'
    id = db.Column(db.Integer, primary_key=True)


class Location(db.Model):
    """Stores the location & time"""
    __tablename__ = 'Locations'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('People.id'))

    #This stores the long, lat and time.
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    time = db.Column(db.String(16))

    # Relationship store the person's locations as a list in the person's table in the people table.
    person = db.relationship(
        'Person',
        backref=db.backref('Locations', lazy='dynamic', collection_class=list)
    )


if __name__ == "main":
    db.create_all()