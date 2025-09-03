from spudoolicom import app, db, forms, config
from flask import render_template, request, flash, redirect, abort
import exifread
from datetime import datetime
from flask_wtf.csrf import CSRFProtect, CSRFError
import re
import os

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


@app.route('/photoblog-map')
def photoblogmap():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, googlemap FROM pixelpost_pixelpost where googlemap like '%.%'")
    markers = cursor.fetchall()
    cursor.close()
    return render_template('photoblog-map.html', markers = markers)


@app.route('/photoblog', strict_slashes=False, defaults={'id': None} )
@app.route('/photoblog/<id>', methods=('GET', 'POST'))
def post(id):

    if id is None:
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id FROM pixelpost_pixelpost order by id DESC LIMIT 1")
        latestpost = cursor.fetchone()
        id = latestpost[0]

    # If something nefarious in the URL, redirect to a page 
    x = re.search('[a-zA-Z]', str(id))
    if x:
        return redirect('/photoblog', code=301)

    # Get the post
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, body, datetime, googlemap, alt_text FROM pixelpost_pixelpost where id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    if post is None:
        abort(404)

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

    if "EXIF DateTimeOriginal" in tags:
        # TODO: fix this date to be a human friendly date
        captured = tags["EXIF DateTimeOriginal"]
    else:
        captured = ""

    exifhtml = f'{imagemodel} - {exposuretime} sec, f{fstop} at {focallength}mm'

    #check of there is a large image version of imagename[1] in the directory and if so, set image+exists to true
    if os.path.isfile("/var/www/spudooli/spudoolicom/static/photoblog/embiggen/embiggen_" + imagename[1]):
        imageexists = True  
    else:
        imageexists = False

    # If there is lat and lon in the database, display a map on the post
    if post[5]:
        latlon = post[5]
        photolat = str(latlon.split(",")[0].replace("(", ""))
        photolon = str(latlon.split(",")[1].replace(" ","").replace(")",""))
        maprequest = "<a href='https://www.google.co.nz/maps/@" + photolat + "," + photolon + ",16.0z'><img src='https://maps.googleapis.com/maps/api/staticmap?center=" + photolat + "," + photolon + "&zoom=15&size=350x300&markers=color:0xD0E700%7Clabel:X%7C" + photolat + "," + photolon +  "&sensor=false&key=" + config.googlemapsapikey + "&visual_refresh=true&maptype=terrain' class='img-fluid' alt='Map of the photo location'></a>"
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

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id FROM pixelpost_pixelpost order by id DESC LIMIT 1")
    latestpost = cursor.fetchone()
    latestpost = latestpost[0]
    if int(id) < int(latestpost):
        cursor.execute("SELECT id FROM pixelpost_pixelpost where id > %s order by id LIMIT 1", (id,))
        nextimage = cursor.fetchone()
        nextimage = nextimage[0]
    else:
        nextimage = "nopost"
  
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
            if "thesis" in commenturl:
                flash("Sod off spammer")
            elif id == "110" or id == "66" or id == "348":
                flash("Sod off spammer")
            elif "euroopera" in commenturl:
                flash("Sod off spammer")
            else:
                cur = db.mysql.connection.cursor()
                cur.execute("select email from approved_commenter where email = %s", (commentemail,))
                approved = cur.fetchone()
                if approved == None:
                    publishcomment = "no"
                else:
                    publishcomment = "yes"
                cur.execute("INSERT INTO pixelpost_comments (parent_id, message, name, url, email, datetime, publish) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (id, commentmessage, commentname, commenturl, commentemail, commentdate, publishcomment))
                db.mysql.connection.commit()
                cur.close()

                flash("We got your comment, we'll consider publishing it in due course")
                return redirect('/photoblog/' + id, code=301)

    return render_template('post.html', post = post, id = id, comments = comments, maprequest = maprequest, 
                            exifhtml = exifhtml, captured = captured, previousimage = previousimage, 
                            nextimage = nextimage, form = form, imageexists = imageexists)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('404.html', reason=e.description), 400