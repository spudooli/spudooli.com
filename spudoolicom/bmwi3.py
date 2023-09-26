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

    return render_template('bmwi3.html', totalkwh = totalkwh, totalcost = totalcost, i3traveled = i3traveled, costperkm = costperkm)
    

