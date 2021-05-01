
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
#from flaskr.test_data import x_y_tuples
from flask import json as flask_json
import json
from numpy import sqrt
from os import path
from datetime import datetime
import time


GoogleMaps(app)

@app.route('/')
@app.route('/intro')
def intro(name=None):
    #Home page
    return render_template('intro.html', name=name)

@app.route('/mapview/<x>/<y>/<d>/<t>', methods=['GET', 'POST'])
def map(x,y,t,d):
    #Return a new rendered template
    #return render_template('mapview.html', mymap=mymap, sndmap=sndmap)
    #This takes the data for google maps. You have to parse URL arguments.
    x = float(x)
    y = float(y)
    t = t
    d = d
    return render_template('mapview.html', date = d, time = t, center_x=x, center_y=y, api_key=app.config['GOOGLEMAPS_KEY'])

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
            # Add to locations
            person.Locations.append(location)
            # creating a map in the view
        # Render time as day
        DTime = person.Locations[0].time
        d = 0
        t = 0
        try:
            if(len(DTime) != 16):
                raise ValueError
            clocktime = DTime[11:]
            date = DTime[:10]
            pattern_date = "%m/%d/%Y"
            pattern_time = "%H:%M"
            d = int(time.mktime(time.strptime(date,pattern_date))//86400)
            t = time.strptime(clocktime,pattern_time)
            t = round((t[3]*60 + t[4]) / 30) * 30
        except (OverflowError, ValueError):
            d = 0
            t = 480
            flash(u"Invalid datetime, defaulting to 0, 480",'error')

        return redirect(url_for('map',x=person.Locations[0].latitude,y=person.Locations[0].longitude,
                                t=t,d=d))

    
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

@app.route('/generatemap/<dirname>/<filename>',methods=['GET','POST'])
def generate_hotspots(filename="t480.json",dirname='0'):
    filename = path.join(app.root_path+'/data/day'+dirname+'/t'+filename+'.json')
    hotspots = {}
    hs_num = 0
                            # 0.0001 for 36 foot radius and 0.0002 for
    PROXIMITY = 0.000001    # 100 foot radius, thereabouts
    FORM = 10               # scale for degree decimal used in data
    PROXIMITY = PROXIMITY * FORM
    c = 'coord'
    pos = 'pos'
    try:
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
    except (IOError):
        return {}
    # Return latitude and longitude coords
    headers = {"Content-Type" : "application/json"}
    return make_response(
        hotspots
    )