from flask import render_template
from spudoolicom import app, db
import json
import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)


def statusFile(thing):
    jsonFile = open("/var/www/scripts/statusfile.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    return data[thing]

@app.route('/house')
def house():

    indoortemp = r.get('indoorTemperature') + "&deg;"
    outdoortemp = r.get('outdoorTemperature') + "&deg;"
    indoorHigh = statusFile("indoorHigh") + "&deg;"
    indoorLow = statusFile("indoorLow") + "&deg;"
    outdoorHigh = statusFile("outdoorHigh") + "&deg;"
    outdoorLow = statusFile("outdoorLow") + "&deg;"
    shedtemp = r.get('gardenshedTemperature') + "&deg;"
    mancaveTemperature = r.get('mancaveTemperature') + "&deg;"
    kitchenTemperature = r.get("kitchenTemperature") + "&deg;"
    kitchenhumidity = r.get("kitchenHumidity") + "%"
    centralheating = r.get("heatTemperature") + "&deg;"
    centralheatinghumidity = r.get("heatHumidity") + "%"
    fridgedoortoday = statusFile("fridgeDoorCounter")
    barometer = r.get("indoorPressure")
    barometer = barometer[0:-2]

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
    
    return render_template('house.html', waterTemp = waterTemp, barometer = barometer, fridgedoortoday = fridgedoortoday, 
                          kitchenhumidity = kitchenhumidity, kitchenTemperature = kitchenTemperature, centralheatinghumidity = centralheatinghumidity, 
                          shedtemp = shedtemp, centralheating = centralheating, mancaveTemperature = mancaveTemperature, fridgeDoorCount = fridgeDoorCount, 
                          indoortemp = indoortemp, outdoortemp = outdoortemp, indoorHigh = indoorHigh, indoorLow = indoorLow, outdoorHigh = outdoorHigh, 
                          outdoorLow = outdoorLow)
    