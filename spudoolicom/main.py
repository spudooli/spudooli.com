from spudoolicom import app
from flask import render_template
import json


def statusFile(thing):
    jsonFile = open("/var/www/scripts/statusfile.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    return data[thing]


@app.route('/')
def main():

    #Return the number of photos
    f = open("/var/www/scripts/power.txt", "r")    
    power = f.read()
    power = power.split(",")[0]

    # return the bank balance
    f = open("/var/www/scripts/otherbalance.txt", "r")    
    bankbalance = f.read()
    bankbalance = "$" + bankbalance.split(".")[0]

    indoortemp = statusFile("indoorTemperature") + "&deg;"



    return render_template('index.html', bankbalance = bankbalance, power = power, indoortemp = indoortemp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.route("/power")
def power():
    f = open("/var/www/scripts/power.txt", "r")    
    power = f.read()
    power = power.split(",")[0]
    return power 