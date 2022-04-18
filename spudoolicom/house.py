from flask import render_template
from spudoolicom import app, db
import json

def statusFile(thing):
    jsonFile = open("/var/www/scripts/statusfile.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    return data[thing]

@app.route('/house')
def house():

    indoortemp = statusFile("indoorTemperature") + "&deg;"
    outdoortemp = statusFile("outdoorTemperature") + "&deg;"
    indoorHigh = statusFile("indoorHigh") + "&deg;"
    indoorLow = statusFile("indoorLow") + "&deg;"
    outdoorHigh = statusFile("outdoorHigh") + "&deg;"
    outdoorLow = statusFile("outdoorLow") + "&deg;"
    shedtemp = statusFile("gardenshedTemperature") + "&deg;"
    mancaveTemperature = statusFile("mancaveTemperature") + "&deg;"
    kitchenTemperature = statusFile("kitchenTemperature") + "&deg;"
    kitchenhumidity = statusFile("kitchenHumidity") + "%"
    centralheating = statusFile("heatTemperature") + "&deg;"
    centralheatinghumidity = statusFile("heatHumidity") + "%"
    fridgedoortoday = statusFile("fridgeDoorCounter")

    jsonFile = open("/var/www/scripts/spa-temperature.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    waterTemp = round(data["WaterTemp"], 2)
    if waterTemp == 0:
        waterTemp = "-"


    # Fridge door count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(open_count) FROM fridge_door")
    fridgeDoorCount = cur.fetchone()
    unformattedFridgeDoorCount = fridgeDoorCount[0]
    fridgeDoorCount = int(unformattedFridgeDoorCount) + int(fridgedoortoday)
    fridgeDoorCount = "{:,}".format(fridgeDoorCount)
    cur.close()            
    
    return render_template('house.html', waterTemp = waterTemp, fridgedoortoday = fridgedoortoday, kitchenhumidity = kitchenhumidity, kitchenTemperature = kitchenTemperature, centralheatinghumidity = centralheatinghumidity, shedtemp = shedtemp, centralheating = centralheating, mancaveTemperature = mancaveTemperature, fridgeDoorCount = fridgeDoorCount, indoortemp = indoortemp, outdoortemp = outdoortemp, indoorHigh = indoorHigh, indoorLow = indoorLow, outdoorHigh = outdoorHigh, outdoorLow = outdoorLow)
    