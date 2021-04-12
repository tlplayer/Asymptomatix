
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

@app.route('/')
@app.route('/intro')
def intro(name=None):
    #Home page
    return render_template('intro.html', name=name)

@app.route('/analytics')
def analytics(name=None):
    #Analytics Page
    return render_template('analytics.html',name=name)

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

            # Add to locations
            new_person.Locations.append(new_location)

        db.session.commit()

    return render_template(
        'report.html',
        form=form,
        _template=template_form
        )
