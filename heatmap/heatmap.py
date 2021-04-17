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
#
#
# Wrap into a function for flask webpage
#
#
from numpy import sqrt
import json
def euclidean_distance(x,y):
    return sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)

def midpoint(p1,p2):
    return ((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)


def generate_hotspots(filename="./data/exampledata.json"):
    hotspots = []
                            # 0.0001 for 36 foot radius and 0.0002 for
    PROXIMITY = 0.0001      # 100 foot radius, thereabouts
    FORM = 10000            # scale for degree decimal used in data
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
                if(euclidean_distance(data[i][c],data[j][c]) < PROXIMITY):
                    hotspots.append(midpoint(data[i][c],data[j][c]))
    # Return latitude and longitude coords
    print('{} elements'.format(len(hotspots)))
    return hotspots

if(__name__ == '__main__'):
    import os,sys
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    os.chdir('..')
    print("Current directory: ",os.getcwd())
    print(generate_hotspots('./data/day0/t480.json'))
