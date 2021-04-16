
'''
Maintainer: Timothy Player
Date: Mar. 18 2021
Description this hosts the routess to locations on our website. Navigate to routes 
by the URL or links.
'''

# This file holds the URLs and the logic for each.
from flask import render_template, flash, redirect, url_for
from markupsafe import escape
from flaskr import app
from flaskr import geoform
from flaskr import db
from flaskr import database
from flask_googlemaps import Map
from flaskr import GoogleMaps
from flaskr.test_data import x_y_tuples

GoogleMaps(app)

@app.route('/')
@app.route('/intro')
def intro(name=None):
    #Home page
    return render_template('intro.html', name=name)

@app.route('/mapview/<x>/<y>', methods=['GET', 'POST'])
def map(x,y):
    #Return a new rendered template
    #return render_template('mapview.html', mymap=mymap, sndmap=sndmap)
    #This takes the data for google maps. You have to parse URL arguments.
    x = float(x)
    y = float(y)
    coords = [[x[0],x[1]] for x in x_y_tuples]
    return render_template('mapview.html',
            coords=coords, center_x=x, center_y=y, api_key=app.config['GOOGLEMAPS_KEY'])

@app.route('/analytics', methods=['GET', 'POST'])
def analytics(name=None):
    #Analytics Page
    form = geoform.MainForm()
    template_form = geoform.GeoForm(prefix='Locations-_-')

    #This is how you access location data
    #print(patient0.Locations[0].latitude)
    
    #When the user hits search the can see all the at risk places nearby where they were.
    if form.validate_on_submit():
        person = database.Person()

        for location in form.locations.data:
            location = database.Location(**location)
            print(location)
            # Add to locations
            person.Locations.append(location)
            # creating a map in the view
        print(person.Locations[0])
        return redirect(url_for('map',x=person.Locations[0].latitude,y=person.Locations[0].longitude))

    
    return render_template(
        'analytics.html',
        form=form, #This is the main form
        _template=template_form, #Location Form
        ) 
   

@app.route('/report', methods=['GET', 'POST'])
def form(name=None):
    form = geoform.MainForm()
    template_form = geoform.GeoForm(prefix='Locations-_-')

    if form.validate_on_submit():
        # Create person
        new_person = database.Person()

        db.session.add(new_person)

        for location in form.locations.data:
            new_location = database.Location(**location)
            print(location)
            # Add to locations
            new_person.Locations.append(new_location)


        db.session.commit()

    return render_template(
        'report.html',
        form=form,
        _template=template_form
        )
