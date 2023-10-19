from spudoolicom import app, db
from flask import render_template
from datetime import datetime

import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

@app.route('/i3')
def i3():
    cursor = db.mysql.connection.cursor()
    cursor.execute("select sum(kwh) from i3charging")
    totalkwh = round(int(cursor.fetchone()[0]) / 1000, 2)
    cursor.close()

    cursor = db.mysql.connection.cursor()
    cursor.execute("select sum(cost) from i3charging")
    totalcost = round(float(cursor.fetchone()[0]), 2)
    cursor.close()

    i3traveled = int(r.get('i3mileage')) - int(46683)

    costperkm = round(int(totalcost) / int(i3traveled) * 100, 2)

    # Count the number of lines in the file
    with open('/var/www/scripts/i3-location.txt', 'r') as f:
        i3pings = len(f.readlines())

    # Get all months spent on petrol
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM chargedate) thismonth, sum(cost) as warehouse FROM i3charging GROUP BY thismonth order by thismonth asc")
    data = cur.fetchall()
    chargelabels = [row[0] for row in data]
    chargevalues = [str(row[1]).replace("-","") for row in data]
    cur.close()  

    return render_template('bmwi3.html', totalkwh = totalkwh, totalcost = totalcost, i3traveled = i3traveled, costperkm = costperkm, i3pings = i3pings, chargelabels = chargelabels, chargevalues = chargevalues)
    

