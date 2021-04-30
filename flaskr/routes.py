
'''
Maintainer: Timothy Player
Date: Mar. 18 2021
Description this hosts the routess to locations on our website. Navigate to routes 
by the URL or links.
'''

# This file holds the URLs and the logic for each.
from flask import render_template, flash, redirect, url_for, make_response
from markupsafe import escape
from flaskr import app
from flaskr import geoform
from flaskr import db
from flaskr import database
from flask_googlemaps import Map
from flaskr import GoogleMaps
from flaskr.test_data import x_y_tuples
from flask import json as flask_json
import json
from numpy import sqrt
from os import path


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

@app.route('/generatemap/<filename>',methods=['GET','POST'])
def generate_hotspots(filename="./data/exampledata.json"):
    filename = path.join(app.root_path+'/data/day0/'+filename)
    hotspots = {}
    hs_num = 0
                            # 0.0001 for 36 foot radius and 0.0002 for
    PROXIMITY = 0.000001    # 100 foot radius, thereabouts
    FORM = 10               # scale for degree decimal used in data
    PROXIMITY = PROXIMITY * FORM
    c = 'coord'
    pos = 'pos'
    with open(filename,'r') as f:
        data = json.load(f)
    data = sorted(data,key=lambda x: (x[c][0],x[c][1]))
    for i in range(len(data)):
        if(data[i][pos]):
            # Scan the people within PROXIMITY to determine possible infection
            search_width = 10
            start = -1
            # Iteratively increase the number of people we need to search over
            # Order logN  * n for determining infections. Better than n^2
            while(not(i - search_width <= 0)):
                if(data[i-search_width][c][0] < data[i][c][0] - PROXIMITY):
                    start = i-search_width
                    break
                search_width *= 2
            if(start == -1):
                start = 0
            end = -1
            search_width = 10
            while(not(i + search_width >= len(data)-1)):
                if(data[i-search_width][c][0] > data[i][c][0] + PROXIMITY):
                    end = i+search_width
                    break
                search_width *= 2
            if(end == -1):
                end = len(data)-1

            # If there is a possible exposure, add exposure midpoint
            for j in range(start,end):
                y = data[j][c]
                x = data[i][c]
                if(sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2) < PROXIMITY):
                    # Add lat,long as tuple to meaningless incrementing int key, to return as dict
                    hotspots[hs_num] = ((x[0]+y[0])/2,(x[1]+y[1])/2)
                    hs_num += 1
    # Return latitude and longitude coords
    headers = {"Content-Type" : "application/json"}
    return make_response(
        hotspots
    )