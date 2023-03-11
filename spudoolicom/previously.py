from flask import render_template, redirect
from spudoolicom import app, db
from datetime import date
import datetime
import re


@app.route('/previously', strict_slashes=False)
def previously():

   
    return render_template('previously.html', )
