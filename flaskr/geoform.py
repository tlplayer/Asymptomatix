from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, FloatField, SelectField, \
        StringField, TextAreaField, SubmitField
from wtforms import validators, fields


class GeoForm(Form):
    """Sub Form
        This takes the longitude and latitude of the user's that are positve for covid for the last couple of days.
    """
    longitude = FloatField(
        'Longitude',
        validators=[validators.InputRequired()]
    )
    latitude = FloatField(
        'Latitude',
        validators=[validators.InputRequired()]
    )
    #Year month day format
    time = StringField(
        'Date (MM/DD/YYYY HH:MM)',
        validators=[validators.InputRequired(), validators.Length(min=16,max=16)]
    ) 


class MainForm(FlaskForm):
    """Parent form. Takes 1-20 forms"""
    locations = FieldList(
        FormField(GeoForm),
        min_entries=1,
        max_entries=20
    )