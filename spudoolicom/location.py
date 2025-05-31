from spudoolicom import app, db
from flask import render_template

@app.route('/location')
def location():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 4 ORDER BY `id` DESC limit 1")
    gabbalocation = cursor.fetchone()
    cursor.close()
    gabbaupdated = str(gabbalocation[1])
    gabbamap = str(gabbalocation[8])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 3 ORDER BY `id` DESC limit 1")
    davelocation = cursor.fetchone()
    cursor.close()
    daveupdated = str(davelocation[1])
    davemap = str(davelocation[8])


    return render_template('location.html', 
                           gabbamap=gabbamap,
                           davelocation=davelocation,
                           davemap=davemap,
                           gabbaupdated=gabbaupdated,
                           daveupdated=daveupdated)
    

