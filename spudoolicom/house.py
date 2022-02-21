from spudoolicom import app, db
from flask import request, render_template

@app.route('/house')
def house():
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(count) FROM catflap")
    catflapCount = cur.fetchone()
    cur.close()

    
    return render_template('house.html', catflapCount = catflapCount)
    