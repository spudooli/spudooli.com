from spudoolicom import app, db
from flask import render_template
import pytz
from datetime import datetime
import os
import platform

def get_creation_time(file_path):
        stat = os.stat(file_path)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


@app.route('/sarah')
def sarahjapan():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 7 ORDER BY `id` DESC limit 1")
    sarahjapanlocation = cursor.fetchone()
    cursor.close()
    sarahjapanupdated = str(sarahjapanlocation[1])
    sarahjapanlatlon = str(sarahjapanlocation[3]) + "," + str(sarahjapanlocation[4])
    sarahjapanlocation = "<img src='https://maps.googleapis.com/maps/api/staticmap?center=" + sarahjapanlatlon + "&zoom=12&size=640x640&scale=2&markers=color:0xD0E700%7Clabel:SC%7C" + sarahjapanlatlon + "&sensor=false&key=AIzaSyCyuhLhlvQCW7dZBaA5-HLzDP6Sau-qmvA&visual_refresh=true&maptype=terrain'  class='img-fluid' ><p>Updated: " + sarahjapanupdated + "</p>"

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `track` where who = 7 and date > '2024-01-01'")
    sarahjapanpingcount = cursor.fetchone()[0]
    cursor.close()

    target_timezone = pytz.timezone('Asia/Tokyo')
    local_time = datetime.now()
    sarah_time = local_time.astimezone(target_timezone)
    sarah_formatted_datetime_str =sarah_time.strftime("%d/%m/%Y %H:%M:%S")


    return render_template('sarah.html', sarahjapanlocation = sarahjapanlocation, sarahjapanpingcount = sarahjapanpingcount, sarah_formatted_datetime_str = sarah_formatted_datetime_str)
