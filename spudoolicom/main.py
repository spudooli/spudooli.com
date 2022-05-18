from turtle import down
from spudoolicom import app, db
from flask import render_template, make_response, redirect, request
import json
from datetime import datetime
import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)


@app.route('/')
def main():

    # Return the power usage
    power = r.get('power')


    # return the bank balance
 
    bankbalance = r.get('bankbalance')
    bankbalance = "$" + bankbalance.split(".")[0]

    indoortemp = r.get('indoorTemperature') + "&deg;"

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
    if thexarg == "browse":
        return redirect("/photblog/archive", code=301)

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
    cursor.execute("SELECT topic, statusdatetime, downtime FROM status ORDER BY topic ASC")
    statii = cursor.fetchall()
    cursor.close()
    rightnow = datetime.now()
    topicstatus = []
    for topic in statii:
        upornot = (rightnow - topic[1]).seconds
        if upornot < topic[2]:
            upornot = "good"
        else:
            upornot = "-"
        topicstatus.append([topic[0], upornot, topic[1]])


    return render_template('status.html', statii = statii, rightnow = rightnow, topicstatus = topicstatus)

@app.route('/about')
def about():
   return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route("/power")
def power():
    power = r.get('power')
    return power 


