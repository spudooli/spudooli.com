from flask import render_template
from spudoolicom import app, db
import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)


@app.route('/house')
def house():

    indoortemp = r.get('indoorTemperature') + "&deg;"
    outdoortemp = r.get('outdoorTemperature') + "&deg;"
    outdoorhumidity = r.get('outsideHumidity') + "%"
    shedtemp = r.get('gardenshedTemperature') + "&deg;"
    mancaveTemperature = r.get('mancaveTemperature') + "&deg;"
    mancavehumidity = r.get("mancaveHumidity") + "%"
    kitchenTemperature = r.get("kitchenTemperature") + "&deg;"
    kitchenhumidity = r.get("kitchenHumidity") + "%"
    centralheating = r.get("heatTemperature") + "&deg;"
    centralheatinghumidity = r.get("heatHumidity") + "%"
    fridgedoortoday = r.get("fridgeDoorCounter")
    barometer = r.get("indoorPressure")
    barometer = barometer[0:-2]
    i3range = r.get("i3rangeremaining")
    i3battery = r.get("i3batteryremaining")

    waterTemp = r.get('spatemperature')
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
                          indoortemp = indoortemp, outdoortemp = outdoortemp, outdoorhumidity = outdoorhumidity, mancavehumidity = mancavehumidity, i3range = i3range, i3battery = i3battery)
    