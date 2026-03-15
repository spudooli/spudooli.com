from flask import render_template
from spudoolicom import app, db
import redis

r = redis.from_url(app.config['REDIS_URL'], encoding="utf-8", decode_responses=True)


@app.route('/house')
def house():

    indoortemp = (r.get('indoorTemperature') or "?") + "&deg;"
    outdoortemp = (r.get('outdoorTemperature') or "?") + "&deg;"
    outdoorhumidity = (r.get('outsideHumidity') or "?") + "%"
    shedtemp = (r.get('gardenshedTemperature') or "?") + "&deg;"
    mancaveTemperature = (r.get('mancaveTemperature') or "?") + "&deg;"
    mancavehumidity = (r.get("mancaveHumidity") or "?") + "%"
    kitchenTemperature = (r.get("kitchenTemperature") or "?") + "&deg;"
    kitchenhumidity = (r.get("kitchenHumidity") or "?") + "%"
    centralheating = (r.get("heatTemperature") or "?") + "&deg;"
    centralheatinghumidity = (r.get("heatHumidity") or "?") + "%"
    fridgedoortoday = r.get("fridgeDoorCounter") or "0"
    barometer = r.get("indoorPressure") or "0hPa"
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
    
