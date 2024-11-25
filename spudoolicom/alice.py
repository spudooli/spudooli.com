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

def list_files_by_creation_date(directory):
    files = os.listdir(directory)
    files = [os.path.join(directory, file) for file in files]
    files.sort(key=get_creation_time)
    return files

@app.route('/alice-in-europe')
def alicelocation():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 5 ORDER BY `id` DESC limit 1")
    alicelocation = cursor.fetchone()
    cursor.close()
    aliceupdated = str(alicelocation[1])
    alicelatlon = str(alicelocation[3]) + "," + str(alicelocation[4])
    alicelocation = "<img src='https://maps.googleapis.com/maps/api/staticmap?center=" + alicelatlon + "&zoom=12&size=640x640&scale=2&markers=color:0xD0E700%7Clabel:A%7C" + alicelatlon + "&sensor=false&key=AIzaSyCyuhLhlvQCW7dZBaA5-HLzDP6Sau-qmvA&visual_refresh=true&maptype=terrain'><p>Updated: " + aliceupdated + "</p>"

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `track` where who = 5")
    alicepingcount = cursor.fetchone()[0]
    cursor.close()

    image_dir = '/var/www/spudooli/spudoolicom/static/images/alice-in-europe'
    files_by_creation_date = list_files_by_creation_date(image_dir)

    image_files = [f for f in files_by_creation_date]  

    target_timezone = pytz.timezone('Europe/Paris')
    local_time = datetime.now()
    alice_time = local_time.astimezone(target_timezone)
    alice_formatted_datetime_str = alice_time.strftime("%d/%m/%Y %H:%M:%S")


    return render_template('alice-in-europe.html', alicelocation = alicelocation, alicepingcount = alicepingcount, image_files = image_files, alice_formatted_datetime_str = alice_formatted_datetime_str)
    
@app.route('/alice')
def aliceuk():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT * FROM `track` where who = 6 ORDER BY `id` DESC limit 1")
    aliceuklocation = cursor.fetchone()
    cursor.close()
    aliceukupdated = str(aliceuklocation[1])
    aliceuklatlon = str(aliceuklocation[3]) + "," + str(aliceuklocation[4])
    aliceuklocation = "<img src='https://maps.googleapis.com/maps/api/staticmap?center=" + aliceuklatlon + "&zoom=12&size=640x640&scale=2&markers=color:0xD0E700%7Clabel:A%7C" + aliceuklatlon + "&sensor=false&key=AIzaSyCyuhLhlvQCW7dZBaA5-HLzDP6Sau-qmvA&visual_refresh=true&maptype=terrain'><p>Updated: " + aliceukupdated + "</p>"

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `track` where who = 6 and date > '2024-01-01'")
    aliceukpingcount = cursor.fetchone()[0]
    cursor.close()

    image_dir = '/var/www/spudooli/spudoolicom/static/images/alice-in-uk'
    files_by_creation_date = list_files_by_creation_date(image_dir)

    image_files = [f for f in files_by_creation_date]  

    target_timezone = pytz.timezone('Europe/London')
    local_time = datetime.now()
    alice_uk_time = local_time.astimezone(target_timezone)
    alice_uk_formatted_datetime_str = alice_uk_time.strftime("%d/%m/%Y %H:%M:%S")


    return render_template('alice.html', aliceuklocation = aliceuklocation, aliceukpingcount = aliceukpingcount, image_files = image_files, alice_uk_formatted_datetime_str = alice_uk_formatted_datetime_str)
