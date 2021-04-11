
'''
Maintainer: Timothy Player
Date: Mar. 18 2021
Description this hosts the routess to locations on our website. Navigate to routes 
by the URL.
'''

# This file holds the URLs and the logic for each.
from flask import render_template, flash, redirect, url_for
from markupsafe import escape
from flaskr import app
from flaskr import geoform
from flaskr import db

@app.route('/')
@app.route('/intro')
def intro(name=None):
    #Home page
    return render_template('intro.html', name=name)

@app.route('/analytics')
def analytics(name=None):
    #Analytics Page
    return render_template('analytics.html',name=name)

@app.route('/report', methods=['GET','POST'])
def form(name=None):
    form = MainForm()
    template_form = GeoForm(prefix='Locations')
    if form.validate_on_submit():
        # Create race
        new_location = locations()

        db.session.add(new_location)

        for location in form.locations.data:
            new_location = Locations(**location)

            # Add to race
            new_location.laps.append(new_location)

        db.session.commit()


    locations = Race.query

    return render_template(
        'report.html',
        form=form,
        locations=locations,
        _template=template_form
    )
    #This is where the user supplies info for the JSON
    return render_template('report.html')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)