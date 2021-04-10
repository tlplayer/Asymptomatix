# Asymptomatix
![LOGO](logo.png)

##Description

Asymptomatix is a crowd source covid-19 contact tracing website. In brief, it enables users to submit their last geolocations over the last 2 weeks to a database that can be accessed by users to check hotspots of Covid-19. No name, no signup required. It enables complete anonymity and we rest a lot of trust in the user. So the reported numbers are subject to inaccuracy and fallacy. This is just to help visualize.

##INSTALLATION

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirments.txt
```

Point the FLASK_APP variable at the directory/file that holds the app
```sh
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK
export FLASK_RUN_PORT=8008
```
Run the flask app
```sh
flask run
```
