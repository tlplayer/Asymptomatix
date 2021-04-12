# Docstring
'''
    Script: heatmap.py
    Description: Algortihm which makes hotspot objects for a google maps heatmap plugin for
                 the Asymptomatix project.
    
    Parameters:
        Contact tracing data file in the data directory

    Returns:
        File containing hotspot objects in the data directory
'''




import json
import os
import datetime

PROXIMITY = 10
PROX_LLFRAC = 0.001
PROX = PROXIMITY * PROX_LLFRAC
VAX_EFF = 0.9

class hotspot:
    def __init__(   self,coord=(0.0,0.0),time=datetime.datetime(0,0,0,0,),time_int=0,\
                    radius=15,scaleRadius=True,useLocalExtrema=False):
        self.coord = coord
        self.radius = radius
        self.scaleRadius = scaleRadius
        self.useLocalExtrema = useLocalExtrema

os.chdir('..')
filename = 'fake_CT10000_wvax.json'
datafile = './data/'+filename
with open(datafile,'r') as f:
    data = json.load(f)

