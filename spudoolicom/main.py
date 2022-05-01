from spudoolicom import app, db
from flask import render_template, make_response
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

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM pixelpost_pixelpost")
    imagecount = cursor.fetchone()
    imagecount = imagecount[0]
    cursor.close()

    return render_template('index.html', imagecount = imagecount, bankbalance = bankbalance, power = power, indoortemp = indoortemp)

@app.route('/rss')
def rss():
    # Get latest 10 posts for RSS feed 
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, body, datetime FROM pixelpost_pixelpost ORDER BY id DESC LIMIT 10")
    posts = cursor.fetchall()
    cursor.close()
    rss_xml = render_template('feed.rss', posts = posts)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route("/power")
def power():
    f = open("/var/www/scripts/power.txt", "r")    
    power = f.read()
    power = power.split(",")[0]
    return power 