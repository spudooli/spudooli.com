from flask import Flask
from datetime import datetime
import logging

app = Flask(__name__, static_folder='static')

from . import auth
app.register_blueprint(auth.bp)

app.config.from_pyfile('config.py')

handler = logging.FileHandler('/tmp/spudoolicom.log')  
handler.setLevel(logging.ERROR)  
app.logger.addHandler(handler)  

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
import spudoolicom.auth