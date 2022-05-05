from spudoolicom import app, db
from flask import render_template, make_response, redirect, request
import json
from datetime import datetime


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

# Handle old URLs - Make a redirect to the new place
@app.route('/index.php')
def redirectthings():
    args = request.args
    thexarg = args.get('x')
    if thexarg == "rss":
        return redirect("/rss", code=301)

    return redirect("/", code=301)

@app.route('/rss')
def rss():
    # Get latest 10 posts for RSS feed 
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, body, datetime, image FROM pixelpost_pixelpost ORDER BY id DESC LIMIT 10")
    posts = cursor.fetchall()
    cursor.close()
    rss_xml = render_template('feed.rss', posts = posts)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response

@app.route('/status')
def spudoolistatus():
    # Get latest topics from the database for the status page 
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT topic, statusdatetime FROM status ORDER BY topic ASC")
    statii = cursor.fetchall()
    cursor.close()
    rightnow = datetime.now()
    topicstatus = []
    for topic in statii:
        upornot = (rightnow - topic[1]).seconds
        if upornot < 240:
            upornot = "good"
        else:
            upornot = "-"
        topicstatus.append([topic[0], upornot, topic[1]])


    return render_template('status.html', statii = statii, rightnow = rightnow, topicstatus = topicstatus)

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


