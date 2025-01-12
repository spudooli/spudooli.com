from spudoolicom import app, db
from flask import render_template
from datetime import datetime
import pytz


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

    ruckmsleft = format(65525 - int(r.get('i3mileage')), ',')

    costperkm = round(int(totalcost) / int(i3traveled) * 100, 2)

    i3range = r.get("i3rangeremaining")
    i3battery = r.get("i3batteryremaining")

    i3chargingstatus = r.get('i3chargingstatus')
    if i3chargingstatus == "CHARGING":
        charging = " CHARGING"
        i3chargecompletiontime = r.get('i3chargecompletiontime')
        dete = datetime.fromisoformat(i3chargecompletiontime)
        # Set the timezone to NZ
        nz_tz = pytz.timezone('Pacific/Auckland')
        dt_nz = dete.astimezone(nz_tz)
        i3chargecompletiontime_formatted_time = dt_nz.strftime('%Y-%m-%d %H:%M')
    else:
        charging = ""
        i3chargecompletiontime_formatted_time = "" 

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

    return render_template('bmwi3.html', totalkwh = totalkwh, totalcost = totalcost, i3traveled = i3traveled, costperkm = costperkm, 
                           i3pings = i3pings, chargelabels = chargelabels, chargevalues = chargevalues, i3range = i3range, 
                           i3battery = i3battery, ruckmsleft = ruckmsleft, charging = charging, i3chargecompletiontime_formatted_time = i3chargecompletiontime_formatted_time)
