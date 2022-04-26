from flask import Flask
from datetime import datetime
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config.from_pyfile('config.py')

csrf = CSRFProtect()
csrf.init_app(app)

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


