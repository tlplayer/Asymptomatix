from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/intro')
def intro(name=None):
    #Home page
    return render_template('intro.html', name=name)

@app.route('/analytics')
def analytics(name=None):
    #Analytics Page
    return render_template('analytics.html',name=name)