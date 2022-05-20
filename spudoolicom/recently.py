from flask import render_template
from spudoolicom import app, db
from datetime import date

@app.route('/recently', strict_slashes=False, defaults={'recentlydate': None})
@app.route('/recently/<recentlydate>')
def recently(recentlydate):

    if recentlydate is None:
        today = date.today()
        recentlydate = today.strftime("%Y-%m-%d")


    cur = db.mysql.connection.cursor()
    datestart = f'{recentlydate} 00:00:00'
    dateend = f'{recentlydate} 23:59:59'
    cur.execute("SELECT event_date, name, type, address, artist, album FROM recently where event_date > %s and event_date < %s order by event_date ASC" , (datestart, dateend) )
    data = cur.fetchall()
    cur.close() 

    
    
    return render_template('recently.html', data = data, recentlydate = recentlydate)

                          
