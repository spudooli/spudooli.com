from email.mime import image
from spudoolicom import app, db
from flask import render_template
import exifread

@app.route('/photoblog')
def photoblog():
    # Get all the posts
    # TODO pagination
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, datetime FROM pixelpost_pixelpost ORDER BY id DESC LIMIT 500")
    posts = cursor.fetchall()
    cursor.close()
    return render_template('photoblog.html', posts = posts)


@app.route('/photoblog/<id>')
def post(id):
    # Get the post
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, body, datetime FROM pixelpost_pixelpost where id = %s", (id,))
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
        fstop = tags["EXIF FNumber"]
    else:
        fstop = ""
    if "EXIF FocalLength" in tags:
        focallength = tags["EXIF FocalLength"]
    else:
        focallength = ""

    captured = tags["Image DateTime"]
    exifhtml = str(imagemodel) + " - " + str(exposuretime) + "sec, f" + str(fstop) + " at " + str(focallength) + "mm"

    # Get previous and next Ids
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id FROM pixelpost_pixelpost where id < %s order by id DESC limit 1", (id,))
    previousimage = cursor.fetchone()
    cursor.close()

    if id < "421":
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id FROM pixelpost_pixelpost where id > %s order by id LIMIT 1", (id,))
        nextimage = cursor.fetchone()
        print(nextimage)
        cursor.close()
    else:
        nextimage = "421"
  

    # Get the comments for the post
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, parent_id, datetime, message, name FROM pixelpost_comments where parent_id = %s order by id ASC", (id,))
    comments = cursor.fetchall()
    cursor.close()



    return render_template('post.html', post = post, comments = comments, exifhtml = exifhtml, captured = captured, previousimage = previousimage, nextimage = nextimage)

