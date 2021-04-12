import json
import os
import sys

dirname = os.path.dirname(__file__)
os.chdir(dirname+'/..')
src = 'fake_CT10000_wvax.json'
srcfile = './data/'+src
dst = './data/day'
with open(srcfile,'r') as f:
    data = json.load(f)

running = True
times = data[0]['t']
splitdata = []
for time in times:
    i = times.index(time)
    for element in data:
        if time in element['t']:
            splitdata.append({
                'id' : element['id'],
                'pos' : element['positive'],
                'vax' : element['vaccinated'],
                'coord' : (element['lat'][i],element['lon'][i])
            })
    try:
        dstfile = dst+str(int(time/1440))+'/'
        if not os.path.isdir(dstfile):
            os.mkdir(dstfile)
        dstfile += 't'+str(int(time%1440))+'.json'
        with open(dstfile,'w') as f:
            json.dump(splitdata,f,indent=4)
    except IOError:
        print("Failed to open ",dstfile,file=sys.stderr)
        exit()
    splitdata.clear()