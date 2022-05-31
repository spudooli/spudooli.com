from spudoolicom import app, db, forms, config
from flask import render_template, request, flash, redirect
import exifread
from datetime import datetime
from flask_wtf.csrf import CSRFProtect, CSRFError
import re

csrf = CSRFProtect()
csrf.init_app(app)

@app.route('/photoblog/archive')
def photoblog():
    # Get all the posts
    # TODO pagination
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, datetime FROM pixelpost_pixelpost ORDER BY id DESC LIMIT 500")
    posts = cursor.fetchall()
    cursor.close()
    return render_template('photoblog.html', posts = posts)

@app.route('/photoblog', strict_slashes=False, defaults={'id': None} )
@app.route('/photoblog/<id>', methods=('GET', 'POST'))
def post(id):

    if id is None:
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id FROM pixelpost_pixelpost order by id DESC LIMIT 1")
        latestpost = cursor.fetchone()
        id = latestpost[0]

    #If something nefarious in the URL, redirect to a page
    x = re.search('[a-zA-Z]', str(id))
    if x:
        return redirect('/photoblog', code=301)

    # Get the post
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, body, datetime, googlemap, alt_text FROM pixelpost_pixelpost where id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()

    # Get Exif
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, image FROM pixelpost_pixelpost where id = %s", (id,))
    imagename = cursor.fetchone()
    cursor.close()
    f = open("/var/www/spudooli/spudoolicom/static/photoblog/" + imagename[1], 'rb')
    tags = exifread.process_file(f, details=False)
    if "EXIF ExposureTime" in tags:
        exposuretime = tags["EXIF ExposureTime"]
    else:
        exposuretime = ""
    if "Image Model" in tags:
        imagemodel = tags["Image Model"]
    else:
        imagemodel = ""
    if "EXIF FNumber" in tags:
        fstopthing = str(tags["EXIF FNumber"])
        print(fstopthing)
        if "/" in fstopthing:
            fstop1 = str(fstopthing.split("/")[0] )
            fstop2 = str(fstopthing.split("/")[1])
            fstop = int(fstop1) / int(fstop2)
        else:
            fstop = tags["EXIF FNumber"]
    else:
        fstop = ""
    if "EXIF FocalLength" in tags:
        focallength = tags["EXIF FocalLength"]
    else:
        focallength = ""

    if "Image DateTimeOriginal" in tags:
        # TODO: fix this date to be a human friendly date
        captured = tags["Image DateTimeOriginal"]
    else:
        captured = ""

    exifhtml = f'{imagemodel} - {exposuretime} sec, f{fstop} at {focallength}mm'

    # If there is lat and lon in the database, display a map on the post
    if post[5]:
        latlon = post[5]
        photolat = str(latlon.split(",")[0].replace("(", ""))
        photolon = str(latlon.split(",")[1].replace(" ","").replace(")",""))
        maprequest = "<a href='https://www.google.co.nz/maps/@" + photolat + "," + photolon + ",16.0z'><img src='https://maps.googleapis.com/maps/api/staticmap?center=" + photolat + "," + photolon + "&zoom=15&size=350x300&markers=color:0xD0E700%7Clabel:X%7C" + photolat + "," + photolon +  "&sensor=false&key=" + config.googlemapsapikey + "&visual_refresh=true&maptype=terrain'></a>"
    else:
        maprequest = ""

    # Get previous and next and latest Ids
    if id == "1":
        previousimage = "1"
    else:
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id FROM pixelpost_pixelpost where id < %s order by id DESC limit 1", (id,))
        previousimage = cursor.fetchone()
        previousimage = previousimage[0]


    cursor.execute("SELECT id FROM pixelpost_pixelpost order by id DESC LIMIT 1")
    latestpost = cursor.fetchone()
    latestpost = latestpost[0]
    if int(id) < int(latestpost):
        cursor.execute("SELECT id FROM pixelpost_pixelpost where id > %s order by id LIMIT 1", (id,))
        nextimage = cursor.fetchone()
        nextimage = nextimage[0]
    else:
        nextimage = latestpost
  
    # Get the comments for the post

    cursor.execute("SELECT id, parent_id, datetime, message, name, url FROM pixelpost_comments where parent_id = %s and publish = 'yes' order by id ASC", (id,))
    comments = cursor.fetchall()
    cursor.close()


    form = forms.photoblogComment()
    if request.method == "POST":
        if form.validate():
            commentmessage = request.form["commentmessage"]
            commentname = request.form["commentname"]
            commenturl = request.form["commenturl"]
            commentemail = request.form["commentemail"]
            commentdate = datetime.now()
            cur = db.mysql.connection.cursor()
            cur.execute("INSERT INTO pixelpost_comments (parent_id, message, name, url, email, datetime, publish) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (id, commentmessage, commentname, commenturl, commentemail, commentdate, "no"))
            db.mysql.connection.commit()
            cur.close()

            flash("We got your comment, we'll consider publishing it in due course")

    return render_template('post.html', post = post, id = id, comments = comments, maprequest = maprequest, exifhtml = exifhtml, captured = captured, previousimage = previousimage, nextimage = nextimage, form = form)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('404.html', reason=e.description), 400