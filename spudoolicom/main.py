from operator import contains
from spudoolicom import app, db, forms
from flask import render_template, make_response, redirect, request, send_from_directory, flash
from datetime import datetime
import redis
from werkzeug.security import check_password_hash
from spudoolicom.auth import login_required
from flask_wtf.csrf import CSRFProtect, CSRFError
import logging


r = redis.StrictRedis('localhost', 6379, charset="utf-8",
                      decode_responses=True)


@app.route('/')
def main():

    power = r.get('power')

    bankbalance = r.get('bankbalance')
    bankbalance = "$" + bankbalance.split(".")[0]

    indoortemp = r.get('indoorTemperature') + "&deg;"
    mancaveTemperature = r.get('mancaveTemperature') + "&deg;"

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM pixelpost_pixelpost")
    imagecount = cursor.fetchone()
    imagecount = imagecount[0]

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'LastFM'")
    lastfmcount = cursor.fetchone()
    lastfmcount = "{:,}".format(lastfmcount[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'Swarm'")
    swarmcount = cursor.fetchone()
    swarmcount = "{:,}".format(swarmcount[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'mastodon'")
    mastodoncount = cursor.fetchone()
    mastodoncount = "{:,}".format(mastodoncount[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, body, alt_text FROM pixelpost_pixelpost order by id DESC LIMIT 1")
    latestpost = cursor.fetchone()

    cursor.close()

    return render_template('/index.html', imagecount=imagecount, bankbalance=bankbalance, power=power, indoortemp=indoortemp,
                            latestpost=latestpost, lastfmcount=lastfmcount, swarmcount=swarmcount, mastodoncount=mastodoncount, mancaveTemperature = mancaveTemperature) 


# Handle old URLs - Make a redirect to the new place
@app.route('/index.php')
def redirectthings():
    args = request.args
    thexarg = args.get('x')
    if thexarg == "rss":
        return redirect("/rss", code=301)
    if thexarg == "browse":
        return redirect("/photoblog/archive", code=301)

    return redirect("/", code=301)


@app.route('/rss')
def rss():
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT id, headline, body, datetime, image FROM pixelpost_pixelpost ORDER BY id DESC LIMIT 10")
    posts = cursor.fetchall()
    cursor.close()
    rss_xml = render_template('feed.rss', posts=posts)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


@app.route('/status')
def spudoolistatus():
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT topic, statusdatetime, downtime FROM status ORDER BY topic ASC")
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

    return render_template('status.html', statii=statii, rightnow=rightnow, topicstatus=topicstatus)


@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/now')
def now():
    return render_template('now.html')
    

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    contactform = forms.contact_us()
    if request.method == "POST":
        if contactform.validate():
            contactusmessage = request.form["contactusmessage"]
            contactusname = request.form["contactusname"]
            contactusemail = request.form["contactusemail"]
            contactusdate = datetime.now()
            if "Mok" in contactusemail or "ericjones" in contactusemail:
                flash("Please, just stop, Mike, Eric, your message has been deleted", "success")
                return redirect("/contactus")
            else:
                cur = db.mysql.connection.cursor()
                cur.execute("INSERT INTO contactus (contactusmessage, contactusname, contactusemail, contactdate) VALUES (%s, %s, %s, %s)",
                        (contactusmessage, contactusname, contactusemail, contactusdate))
                db.mysql.connection.commit()
                cur.close()

                flash("We got your message, we'll carefully consider our reply.", "success")

                return redirect("/contactus")

    return render_template('contactus.html', contactform=contactform)


@app.route("/power")
def power():
    power = r.get('power')
    return power

@app.route("/cloudservices/giovanni/ipaddress", methods=['GET'])
def ipservices():
    user_agent = request.headers.get('User-Agent')
    if user_agent == "PingerFromGiovannisHome":
        try:
            with open('/tmp/cloudservices.log', 'r') as file:
                lines = file.readlines()
                last_10_lines = ''.join(lines[-10:])  
            return last_10_lines, 200, {'Content-Type': 'text/plain'}
        except FileNotFoundError:
            return "File not found.", 404
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Unauthorized User-Agent", 403


@app.route('/robots.txt')
@app.route('/rss.xsl')
@app.route('/humans.txt')
@app.route('/.well-known/security.txt')
@app.route('/sitemap.xml')
@app.route('/radar.gif')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    #logging.exception(e)
    app.logger.exception(e)
    return render_template('500.html'), 500
