from spudoolicom import app, db
from flask import request
import requests
import shutil
import random
import string

import paho.mqtt.client as paho

broker = "192.168.1.2"
port = 1883

def on_connect(client, userdata, flags, reason_code, properties):
   print("Connected With Result Code "+str(reason_code))

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.route("/track/<who>", methods=('GET', 'POST'))
def track(who):
   mapid = get_random_string(8)
   if request.method == "POST":
      if who == "dave":
         whonumber = "3"
      if who == "gabba":
         whonumber = "4"
      if who == "alice":
         whonumber = "6"
      if who == "sarah":
         whonumber = "8"
      request_data = request.get_json()
      type = request_data['_type']
      if type == "location":
         lat = request_data['lat']
         lon = request_data['lon']
         if request_data['alt']:
            alt = request_data['alt']
         else:
            alt = 0
         latlon = str(lat) + ":" + str(lon)
         client1 = paho.Client(paho.CallbackAPIVersion.VERSION2, "websiteTracker")
         client1.connect(broker, port)
         client1.publish("house/location/" + who, latlon)

         if who == "dave" or who == "gabba":
            # Download and save static map image
            www_map_url = f"http://localhost:8080/styles/osm-bright/static/{lon},{lat},16/550x300.png?marker={lon},{lat}|marker-icon.png|scale:0.75"
            try:
               response = requests.get(www_map_url)
               response.raise_for_status() # Raise an exception for bad status codes
               www_file_path = f"/var/www/spudooli/spudoolicom/static/gis/location/{who}_map_{mapid}.png"
               with open(www_file_path, "wb") as f:
                  f.write(response.content)
            except requests.exceptions.RequestException as e:
               print(f"Error downloading map image: {e}")

            dashboard_map_url = f"http://localhost:8080/styles/osm-bright/static/{lon},{lat},16/350x300.png?marker={lon},{lat}|marker-icon.png|scale:0.75"
            try:
               response = requests.get(dashboard_map_url)
               response.raise_for_status() # Raise an exception for bad status codes
               dashboard_file_path = f"/var/www/dashboard.spudooli.com/static/location/{who}_map_{mapid}.png"
               with open(dashboard_file_path, "wb") as f:
                  f.write(response.content)
            except requests.exceptions.RequestException as e:
               print(f"Error downloading map image: {e}")

         cur = db.mysql.connection.cursor()
         cur.execute('''INSERT into track (who, latitude, longitude, altitude, mapid) VALUES (%s, %s, %s, %s, %s)''', (str(whonumber), str(lat), str(lon), str(alt), mapid))
         db.mysql.connection.commit()
         cur.close()
            
   return 'it works'