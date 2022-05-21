from flask import render_template, redirect
from spudoolicom import app, db
from datetime import date
import datetime
import re

@app.route('/recently', strict_slashes=False, defaults={'recentlydate': None})
@app.route('/recently/<recentlydate>')
def recently(recentlydate):

    if recentlydate is None:
        today = date.today()
        recentlydate = today.strftime("%Y-%m-%d")

    #If something nefarious in the URL, redirect to today's date
    x = re.search('[a-zA-Z]', recentlydate)
    if x:
        return redirect('/recently', code=301)
    
    year =  int(recentlydate.split("-")[0])
    month = int(recentlydate.split("-")[1])
    day = int(recentlydate.split("-")[2])
   
    thedate = date(year, month, day)
    prevdate = thedate - datetime.timedelta(days=1)
    nextdate = thedate + datetime.timedelta(days=1)
    if thedate == date.today():
        nextdate = thedate
    humandate = thedate.strftime("%A, %d %B %Y")

    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT created_at, tweet, id FROM amt_tweets where created_at > %s and created_at < %s order by created_at ASC" , (datestart, dateend) )
    tweets = cur.fetchall()
    cur.close() 

    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT event_date, name, type, address, artist, album FROM recently where event_date > %s and event_date < %s order by event_date ASC" , (datestart, dateend) )
    data = cur.fetchall()
    cur.close() 

    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT date, amount FROM bankbalance where date > %s and date < %s order by date ASC" , (datestart, dateend) )
    bankbalance = cur.fetchone()
    cur.close() 

    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT datetime, headline, id FROM pixelpost_pixelpost where datetime > %s and datetime < %s order by datetime ASC" , (datestart, dateend) )
    blogpost = cur.fetchone()
    cur.close() 

    return render_template('recently.html', data = data, recentlydate = recentlydate, prevdate = prevdate, nextdate = nextdate, 
                          humandate = humandate, bankbalance = bankbalance, tweets = tweets, blogpost = blogpost)

                          
