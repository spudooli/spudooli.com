from spudoolicom import app
from flask import request
import paho.mqtt.client as paho

broker = "192.168.1.2"
port = 1883

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

@app.route("/track", methods=['GET'])
def trackapi():
   return 'it works'

@app.route("/track/owntrackdave", methods=['POST'])
def owntrackdave():
   client1 = paho.Client("websiteTrack")
   client1.connect(broker, port)
   request_data = request.get_json()
   type = request_data['_type']
   if type == "location":
      lat = request_data['lat']
      lon = request_data['lon']
      # vel = request_data['vel']
      # alt = request_data['alt']
      latlon = str(lat) + ":" + str(lon)
      client1.publish("house/location/dave", latlon)
   
   return 'it works' 

@app.route("/track/owntrackgabba", methods=['POST'])
def owntrackgabba():
   client1 = paho.Client("websiteTrack")
   client1.connect(broker, port)
   request_data = request.get_json()
   type = request_data['_type']
   if type == "location":
      lat = request_data['lat']
      lon = request_data['lon']
      # vel = request_data['vel']
      # alt = request_data['alt']
      latlon = str(lat) + ":" + str(lon) 
      client1.publish("house/location/gabba", latlon)

   return 'it works'    
    