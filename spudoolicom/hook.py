from spudoolicom import app
from flask import request
import paho.mqtt.client as paho

broker = "192.168.1.2"
port = 1883
client1 = paho.Client("websiteHook")
client1.connect(broker, port)

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)


@app.route("/hook", methods=['POST'])
def hook():
    return 'it works'


@app.route("/hook/lights", methods=['POST'])
def lights():
    request_data = request.get_json()
    device = request_data['device']
    state = request_data['state']

    if device == "livingroomlights":
        if state == "on":
            client1.publish("house/lights/livingroom", "on")
        if state == "off":
            client1.publish("house/lights/livingroom", "off")

    if device == "alllights":
        if state == "on":
            client1.publish("house/lights/all", "on")
        if state == "off":
            client1.publish("house/lights/all", "off")

    if device == "outside":
        if state == "on":
            client1.publish("house/lights/outside", "on")
        if state == "off":
            client1.publish("house/lights/outside", "off")

    if device == "officelights":
        if state == "on":
            client1.publish("house/lights/office", "on")
        if state == "off":
            client1.publish("house/lights/office", "off")

    if device == "kitchenlights":
        if state == "on":
            client1.publish("house/lights/kitchen", "on")
        if state == "off":
            client1.publish("house/lights/kitchen", "off")
    return 'it works'

@app.route("/hook/tv", methods=['POST'])
def tv():
    request_data = request.get_json()
    device = request_data['device']
    state = request_data['state']

    if device == "tv":
        if state == "on":
            client1.publish("house/av/tv", "on")
        if state == "off":
            client1.publish("house/av/tv", "off")   
    return 'it works'

@app.route("/hook/amp", methods=['POST'])
def amp():
    request_data = request.get_json()
    device = request_data['device']
    state = request_data['state']

    if device == "amp":
        if state == "on":
            client1.publish("house/av/amp", "on")
        if state == "off":
            client1.publish("house/av/amp", "off")   

    if device == "zone2":
        if state == "on":
            client1.publish("house/av/zone2", "on")
        if state == "off":
            client1.publish("house/av/zone2", "off")   

    if device == "zone3":
        if state == "on":
            client1.publish("house/av/zone3", "on")
        if state == "off":
            client1.publish("house/av/zone3", "off")   

    return 'it works'