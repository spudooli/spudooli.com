from spudoolicom import app
from flask import render_template
import requests

@app.route('/webcam')
def webcam():


    return render_template('webcam.html', )
    

