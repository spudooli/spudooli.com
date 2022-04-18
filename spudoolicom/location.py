from spudoolicom import app, db
from flask import render_template

@app.route('/location')
def location():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 4 ORDER BY `id` DESC limit 1")
    gabbalocation = cursor.fetchone()
    cursor.close()
    gabbaupdated = str(gabbalocation[1])
    gabbalatlon = str(gabbalocation[3]) + "," + str(gabbalocation[4])
    gabbalocation = "<img src='https://maps.googleapis.com/maps/api/staticmap?center=" + gabbalatlon + "&zoom=15&size=350x300&markers=color:0xD0E700%7Clabel:G%7C" + gabbalatlon + "&sensor=false&key=AIzaSyCyuhLhlvQCW7dZBaA5-HLzDP6Sau-qmvA&visual_refresh=true&maptype=terrain'><p>Updated: " + gabbaupdated + "</p>"

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 3 ORDER BY `id` DESC limit 1")
    davelocation = cursor.fetchone()
    cursor.close()
    daveupdated = str(davelocation[1])
    davelatlon = str(davelocation[3]) + "," + str(davelocation[4])
    davelocation = "<img src='https://maps.googleapis.com/maps/api/staticmap?center=" + davelatlon + "&zoom=15&size=350x300&markers=color:0xD0E700%7Clabel:D%7C" + davelatlon + "&sensor=false&key=AIzaSyCyuhLhlvQCW7dZBaA5-HLzDP6Sau-qmvA&visual_refresh=true&maptype=terrain'><p class='stat_measure' id='current_date' >Updated: " + daveupdated + "</p>"


    return render_template('location.html', gabbalocation = gabbalocation, davelocation = davelocation)
    

