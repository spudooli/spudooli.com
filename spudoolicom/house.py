from os import stat
from spudoolicom import app, db
from flask import request, render_template
import json

def statusFile(thing):
    jsonFile = open("/var/www/scripts/statusfile.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    return data[thing]

@app.route('/house')
def house():
    # Catflap count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(count) FROM catflap")
    catflapCount = cur.fetchone()
    cur.close()

    indoortemp = statusFile("indoorTemperature") + "&deg;"
    outdoortemp = statusFile("outdoorTemperature") + "&deg;"
    indoorHigh = statusFile("indoorHigh") + "&deg;"
    indoorLow = statusFile("indoorLow") + "&deg;"
    outdoorHigh = statusFile("outdoorHigh") + "&deg;"
    outdoorLow = statusFile("outdoorLow") + "&deg;"
    shedtemp = statusFile("gardenshedTemperature") + "&deg;"
    mancaveTemperature = statusFile("mancaveTemperature") + "&deg;"

    # Fridge door count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(open_count) FROM fridge_door")
    fridgeDoorCount = cur.fetchone()
    cur.close()            
    
    return render_template('house.html', catflapCount = catflapCount, shedtemp = shedtemp, mancaveTemperature = mancaveTemperature, fridgeDoorCount = fridgeDoorCount, indoortemp = indoortemp, outdoortemp = outdoortemp, indoorHigh = indoorHigh, indoorLow = indoorLow, outdoorHigh = outdoorHigh, outdoorLow = outdoorLow)
    