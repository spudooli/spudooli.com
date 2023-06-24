from flask import render_template, redirect
from spudoolicom import app, db
from datetime import date
import datetime
import re


@app.route('/projects', strict_slashes=False)
def philosotainment():

   
    return render_template('projects.html', )
