from spudoolicom import app, db
from flask import request

import paho.mqtt.client as paho

broker = "192.168.1.2"
port = 1883

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

@app.route("/track/<who>", methods=('GET', 'POST'))
def track(who):
   if request.method == "POST":
      if who == "dave":
         whonumber = "3"
      if who == "gabba":
         whonumber = "4"
      if who == "alice":
         whonumber = "5"
      request_data = request.get_json()
      type = request_data['_type']
      if type == "location":
         lat = request_data['lat']
         lon = request_data['lon']
         latlon = str(lat) + ":" + str(lon)
         client1 = paho.Client("websiteTracker")
         client1.connect(broker, port)
         client1.publish("house/location/" + who, latlon)

         cur = db.mysql.connection.cursor()
         cur.execute('''INSERT into track (who, latitude, longitude) VALUES (%s, %s, %s)''', (str(whonumber), str(lat), str(lon)))
         db.mysql.connection.commit()
         cur.close()
   return 'it works'  
    
