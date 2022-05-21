from flask import render_template
from spudoolicom import app, db
from datetime import date
import datetime

@app.route('/recently', strict_slashes=False, defaults={'recentlydate': None})
@app.route('/recently/<recentlydate>')
def recently(recentlydate):

    if recentlydate is None:
        today = date.today()
        recentlydate = today.strftime("%Y-%m-%d")
    
    year =  int(recentlydate.split("-")[0])
    month = int(recentlydate.split("-")[1])
    day = int(recentlydate.split("-")[2])
   
    thedate = date(year, month, day)
    print(f'Recently {thedate}')
    prevdate = thedate - datetime.timedelta(days=1)
    nextdate = thedate + datetime.timedelta(days=1)
    if thedate == date.today():
        nextdate = thedate
    print(f'prev {prevdate} , next {nextdate}')
    humandate = thedate.strftime("%B %d, %Y")


    # prevdate = recentlydate - datetime.timedelta(days=1)
    # print(prevdate)

    #previous date to recently date
    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT event_date, name, type, address, artist, album FROM recently where event_date > %s and event_date < %s order by event_date ASC" , (datestart, dateend) )
    data = cur.fetchall()
    cur.close() 

    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT event_date, name, type, address, artist, album FROM recently where event_date > %s and event_date < %s order by event_date ASC" , (datestart, dateend) )
    data = cur.fetchall()
    cur.close() 

    
    
    return render_template('recently.html', data = data, recentlydate = recentlydate, prevdate = prevdate, nextdate = nextdate, humandate = humandate)

                          
