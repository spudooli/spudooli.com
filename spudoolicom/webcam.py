from email.mime import image
from spudoolicom import app, db
from flask import render_template
import requests

@app.route('/webcam')
def webcam():
    response = requests.get("http://192.168.1.194/picture/1/current/")

    file = open("/var/www/spudooli/spudoolicom/static/webcam1.jpg", "wb")
    file.write(response.content)
    file.close()


    return render_template('webcam.html', )
    

