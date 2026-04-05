from spudoolicom import app, db, forms, config, csrf
from flask import render_template, request, flash, redirect, abort
import exifread
from datetime import datetime
from flask_wtf.csrf import CSRFError
import re
import os
import requests

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

    # Count the number of markers
    cursor.execute("SELECT COUNT(*) FROM pixelpost_pixelpost where googlemap like '%.%'")
    mapmarkercount = cursor.fetchone()
    mapmarkercount = mapmarkercount[0]
    cursor.close()

    return render_template('photoblog-map.html', markers = markers, mapmarkercount = mapmarkercount)


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
    def ratio_str_to_float(s):
        if '/' in s:
            num, den = s.split('/')
            return int(num) / int(den)
        return float(s)

    if "EXIF ExposureTime" in tags:
        et_val = ratio_str_to_float(str(tags["EXIF ExposureTime"]))
        if et_val >= 1:
            exposuretime = f"{et_val:.1f}"
        else:
            exposuretime = f"1/{round(1 / et_val)}"
    else:
        exposuretime = ""
    if "Image Model" in tags:
        imagemodel = tags["Image Model"]
    else:
        imagemodel = ""
    if "EXIF FNumber" in tags:
        fstop = f"{ratio_str_to_float(str(tags['EXIF FNumber'])):.1f}"
    else:
        fstop = ""
    if "EXIF FocalLength" in tags:
        focallength = f"{ratio_str_to_float(str(tags['EXIF FocalLength'])):.1f}"
    else:
        focallength = ""
    if "EXIF ISOSpeedRatings" in tags:
        iso = str(tags["EXIF ISOSpeedRatings"])
    else:
        iso = ""

    if "EXIF DateTimeOriginal" in tags:
        captured_str = str(tags["EXIF DateTimeOriginal"])
        try:
            captured_dt = datetime.strptime(captured_str, '%Y:%m:%d %H:%M:%S')
            captured = captured_dt.strftime('%A, %d %B, %Y %H:%M')
        except ValueError:
            captured = captured_str
    else:
        captured = ""

    exif_parts = [str(imagemodel) if imagemodel else "",
                  f"{exposuretime} sec" if exposuretime else "",
                  f"f/{fstop}" if fstop else "",
                  f"{focallength}mm" if focallength else "",
                  f"ISO {iso}" if iso else ""]
    exifhtml = ' - '.join(p for p in exif_parts if p)

    #check of there is a large image version of imagename[1] in the directory and if so, set image+exists to true
    if os.path.isfile("/var/www/spudooli/spudoolicom/static/photoblog/embiggen/embiggen_" + imagename[1]):
        imageexists = True  
    else:
        imageexists = False

    # If there is lat and lon in the database, display a map on the post
    photo_lat = None
    photo_lon = None
    map_img = None
    if post[5]:
        latlon = post[5]
        photo_lat = latlon.split(",")[0].replace("(", "").strip()
        photo_lon = latlon.split(",")[1].replace(")", "").strip()
        local_map_path = os.path.join(app.static_folder, 'images', 'photoblogmaps', str(id) + ".png")
        if not os.path.isfile(local_map_path):
            tile_url = f"http://localhost:8080/styles/osm-bright/static/{photo_lon},{photo_lat},14/550x300.png?marker={photo_lon},{photo_lat}|marker-icon.png"
            try:
                resp = requests.get(tile_url, timeout=5)
                resp.raise_for_status()
                with open(local_map_path, 'wb') as f:
                    f.write(resp.content)
            except requests.exceptions.RequestException:
                pass
        if os.path.isfile(local_map_path):
            map_img = "/static/images/photoblogmaps/" + str(id) + ".png"

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

    return render_template('post.html', post = post, id = id, comments = comments,
                            photo_lat = photo_lat, photo_lon = photo_lon, map_img = map_img,
                            exifhtml = exifhtml, captured = captured, previousimage = previousimage,
                            nextimage = nextimage, form = form, imageexists = imageexists)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('404.html', reason=e.description), 400