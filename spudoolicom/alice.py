from spudoolicom import app, db
from flask import render_template

@app.route('/alice')
def alicelocation():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 5 ORDER BY `id` DESC limit 1")
    alicelocation = cursor.fetchone()
    cursor.close()
    aliceupdated = str(alicelocation[1])
    alicelatlon = str(alicelocation[3]) + "," + str(alicelocation[4])
    alicelocation = "<img src='https://maps.googleapis.com/maps/api/staticmap?center=" + alicelatlon + "&zoom=12&size=1000x1000&markers=color:0xD0E700%7Clabel:A%7C" + alicelatlon + "&sensor=false&key=AIzaSyCyuhLhlvQCW7dZBaA5-HLzDP6Sau-qmvA&visual_refresh=true&maptype=terrain'><p>Updated: " + aliceupdated + "</p>"

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `track` where who = 5")
    alicepingcount = cursor.fetchone()[0]
    cursor.close()

    return render_template('alice.html', alicelocation = alicelocation, alicepingcount = alicepingcount)
    

