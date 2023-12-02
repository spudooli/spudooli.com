from spudoolicom import app, db, forms, config
from flask import render_template, request, flash, redirect, abort
from datetime import datetime
import re

@app.route('/photos', strict_slashes=False)
def albums():
    # Get albums from the albums table
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT albumID, album_name,	album_descr, parent_albumID FROM albums order by albumID DESC")
    albums = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    photoalbums = [dict(zip(column_names, row))
        for row in albums]
    cursor.close()


    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(albumID) FROM images")
    photocount = cursor.fetchone()[0]
    cursor.close()

    return render_template('photos.html', photoalbums = photoalbums, photocount = photocount)


@app.route('/photos/album/<albumid>', methods=('GET', ))
def photos(albumid):
    if albumid is None:
        return redirect('/photos', code=301)
    
    # If something nefarious in the URL, redirect to a page 
    x = re.search('[1-9]', str(albumid))
    if x:
        return redirect('/photos', code=301)
    
    # Get the album
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT albumID, album_name,	album_descr, parent_albumID FROM images where albumID = %s", (albumid,))
    album = cursor.fetchone()
    cursor.close()

    # Get the photos
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT imageID, image_name, image_descr, albumID FROM images where albumID = %s", (albumid,))   
    photos = cursor.fetchall()
    cursor.close()

    return render_template('photoalbum.html', album = album, photos = photos)
    
    
    




