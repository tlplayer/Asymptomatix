'''
Author: Timothy Player
Description:
    This file takes the people from the database and returns a dict containing people
    at their id and at the indices it has the person's locations.
'''

import json
from flaskr import db

def getPeople():
    people = db.query
    data = {}
    for person in people:
        for location in person.locations:
            data[person.id].append(location)

    return json.dump(data)