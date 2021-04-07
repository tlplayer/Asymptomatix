# Fake contact-tracing data template generator
# 03232021 - Adam Bryant - COSC 402 Team 13
import json
import random as rd
import numpy as np
import sys
from enum import Enum
import csv

# The format of the data generated is as follows
# 'id'      - An integer number representing an anonymous patient
# 'positive'- Whether or not a patient is Covid-19 positive
# 'mobility'- Variable corresponding to how much a patient moves
#               Corresponds to alpha(K) in a gamma distribution for movement
# 't'       - List of integers related to sampled timestamps
# 'lat'     - List of integers related to latitude  at timestep, to nearest 10k degree decimal (not arcsecond)
# 'lon'     - List of integers related to longitude at timestep, to nearest 10k degree decimal (not arcsecond)
#
# DOES NOT (YET) CONTAIN
# - Variable number of locations visited. Instead, each person has a "chance" to move
#    based on mobility. Mobility also impacts distance moved.
# - Static "locations", it's just points on a grid right now
# - Handling of people moving off of the grid. Right now, people are confined to the grid points.
# - Any different time control. Right now, we sample everyone at predefined intervals.

# === HEADER ===
class Mobility(Enum):
    HIGH = 5
    MED  = 3
    LOW  = 1
Mob = {}
Mob[Mobility.HIGH] = 'high'
Mob[Mobility.MED]  = 'medium'
Mob[Mobility.LOW]  = 'low'

GRID_BOTTOM_LEFT    = [359443,-839407]
GRID_TOP_RIGHT      = [359611,-839240]
NUM_PATIENTS        = 10000
POSITIVE_PATIENTS   = 100
STEPS               = 24
TIMESTEP            = 30
TIMESTART           = 480
EVERY_POSITIVE      = int(NUM_PATIENTS/POSITIVE_PATIENTS)
# The actual number of vaccinated persons will be approximate
VAX_SAT             = 0.45
EVERY_VAX           = NUM_PATIENTS/(VAX_SAT * NUM_PATIENTS)
print("Number of patients: {}".format(NUM_PATIENTS))
print("\tEvery {}nth person is vaccinated at {} saturation".format(EVERY_VAX,VAX_SAT))
print("\tEvery {}nth person is positive at {} saturation".format(EVERY_POSITIVE,POSITIVE_PATIENTS/NUM_PATIENTS))
VAX_EFFICACY        = 0.9
VAX_RAND_OFFSET     = rd.randint(0,NUM_PATIENTS)

fakeCTfile = "data/fake_CT"+str(NUM_PATIENTS)+"_wvax.json"

jsondata = [{}] * NUM_PATIENTS


def generate_locations(k = 1):
    locations = np.zeros((STEPS,3))
    STARTING_LOCATION = np.array([
        rd.randint(GRID_BOTTOM_LEFT[0],GRID_TOP_RIGHT[0]),
        rd.randint(GRID_BOTTOM_LEFT[1],GRID_TOP_RIGHT[1]),
        TIMESTART
    ])
    locations[0] = STARTING_LOCATION
    for j in range(1,STEPS):
        do_move = rd.randint(1,5)
        loc = np.array([
            locations[j-1][0],
            locations[j-1][1],
            locations[j-1][2]
        ])
        if(k >= do_move):
            movex = rd.gammavariate(k,beta) * rd.choice((-1,1))
            movey = rd.gammavariate(k,beta) * rd.choice((-1,1))
            if(((loc[0] + movex) < GRID_BOTTOM_LEFT[0]) or ((loc[0] + movex) > GRID_TOP_RIGHT[0])):
                movex *= -1
            if(((loc[1] + movey) < GRID_BOTTOM_LEFT[1]) or ((loc[1] + movey) > GRID_TOP_RIGHT[1])):
                movey *= -1
            locations[j] = np.array([
                loc[0] + movex,
                loc[1] + movey,
                loc[2] + TIMESTEP
            ])
        else:
            locations[j] = np.array([
                loc[0],
                loc[1],
                loc[2] + TIMESTEP
            ])
    return locations


for i in range(NUM_PATIENTS):
    # Hidden value for k gamma
    k = rd.randrange(1,6,2)
    beta = 1
    mobility = Mobility(k)

    # Location generation
    # 
    # Location format:
    # location = [
    #   x,y,t  : [XXX,YYY,T]
    # ]
    locations = generate_locations(k)
    vax = bool(rd.random() < VAX_SAT)
    eff = bool(vax and rd.random() < VAX_EFFICACY)
      
    patient = {
        'id' : i,
        'positive' : bool(not(i % EVERY_POSITIVE)),
        'vaccinated' : vax,
        'eff_dose' : eff,
        'mobility' : Mobility(mobility).name,
        't' : list(locations[:,2]),
        'lat' : list(locations[:,0]),
        'lon' : list(locations[:,1])
    }

    jsondata[i] = patient
v = 0
p = 0
e = 0
for element in jsondata:
    if(element['vaccinated'] == True):
        v += 1
        if(element['eff_dose'] == True):
            e += 1
    if(element['positive'] == True):
        p += 1
print("{} people vaccinated ({} effectively), {} people positive".format(v,e,p))
try:
    with open(fakeCTfile,'w') as f:
        json.dump(jsondata,f,indent=4)
except IOError:
    print("Failed to open ",fakeCTfile,file=sys.stderr) 
print("JSON data generation complete")