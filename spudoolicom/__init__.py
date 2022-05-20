from flask import Flask
from datetime import datetime

app = Flask(__name__, static_folder='static')

app.config.from_pyfile('config.py')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


import spudoolicom.main
import spudoolicom.db
import spudoolicom.track
import spudoolicom.hook
import spudoolicom.house
import spudoolicom.photoblog
import spudoolicom.charts
import spudoolicom.money
import spudoolicom.webcam
import spudoolicom.location
import spudoolicom.admin
import spudoolicom.forms
import spudoolicom.search
import spudoolicom.recently


