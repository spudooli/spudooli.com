from flask import Flask, g, request
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler


from flask_caching import Cache

app = Flask(__name__, static_folder='static')
cache = Cache(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

from . import auth
app.register_blueprint(auth.bp)


app.config.from_pyfile('config.py')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


if not app.debug:
    file_handler = RotatingFileHandler('/tmp/spud.log', maxBytes=100240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.WARNING)
    app.logger.info('spudoolicom')


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
import spudoolicom.projects
import spudoolicom.auth
import spudoolicom.weather
import spudoolicom.alice
import spudoolicom.sarah
import spudoolicom.bmwi3
import spudoolicom.photos