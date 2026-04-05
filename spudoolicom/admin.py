from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf.csrf import generate_csrf
from werkzeug.exceptions import abort
from spudoolicom import app, db
import os
import subprocess
from werkzeug.utils import secure_filename
from datetime import datetime
from spudoolicom.auth import login_required
import requests
import random
import string
from flask import jsonify

@app.route("/admin/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"].replace('\n', '<br>')
        photollatlon = request.form["photolatlon"]
        alttext= request.form["alttext"]
        postdate = datetime.now()
        ts = datetime.timestamp(postdate)
        alt_body = " "
        uploaded_file = request.files['file']
        filename = str(ts) + secure_filename(uploaded_file.filename)
        if filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        error = None
        
        convertimage = "convert -define jpeg:size=600x180 \"" + app.config['UPLOAD_PATH'] + filename + "\" -auto-orient  -thumbnail 600x200   -unsharp 0x.5 \"" + app.config['UPLOAD_PATH'] + "/thumbs/thumb_\"" + filename
        os.system(convertimage)

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            cur = db.mysql.connection.cursor()
            cur.execute(
                "INSERT INTO pixelpost_pixelpost (headline, body, image, alt_body, datetime, googlemap, alt_text) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (title, body, filename, alt_body, postdate, photollatlon, alttext))
            db.mysql.connection.commit()
            cur.close()
            return redirect(url_for("photoblog"))

    return render_template("admin-create.html")


@app.route('/admin/posts')
@login_required
def adminposts():
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id, headline, datetime FROM pixelpost_pixelpost order by id DESC LIMIT 500")
        adminposts = cursor.fetchall()
        cursor.close()
        return render_template("admin-posts.html", adminposts = adminposts)


@app.route('/admin/edit/<int:id>', methods=("GET", "POST"))
@login_required
def edit_post(id):
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, body, image, googlemap, alt_text FROM pixelpost_pixelpost WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()

    if post is None:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"].replace('\n', '<br>')
        photolatlon = request.form["photolatlon"]
        alttext = request.form["alttext"]
        uploaded_file = request.files['file']

        if not title:
            flash("Title is required.")
        else:
            if uploaded_file and uploaded_file.filename != '':
                ts = datetime.timestamp(datetime.now())
                filename = str(ts) + secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                convertimage = "convert -define jpeg:size=600x180 \"" + app.config['UPLOAD_PATH'] + filename + "\" -auto-orient  -thumbnail 600x200   -unsharp 0x.5 \"" + app.config['UPLOAD_PATH'] + "/thumbs/thumb_\"" + filename
                os.system(convertimage)
            else:
                filename = post[3]

            cur = db.mysql.connection.cursor()
            cur.execute(
                "UPDATE pixelpost_pixelpost SET headline = %s, body = %s, image = %s, googlemap = %s, alt_text = %s WHERE id = %s",
                (title, body, filename, photolatlon, alttext, id))
            db.mysql.connection.commit()
            cur.close()
            return redirect(url_for("post", id=id))

    # Convert <br> back to newlines for the textarea
    body_for_form = post[2].replace('<br>', '\n')

    return render_template("admin-edit.html", post=post, body_for_form=body_for_form)


@app.route('/admin/comments')
@login_required
def admincomments():
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id, parent_id, datetime, message, name, url, publish FROM pixelpost_comments order by id DESC LIMIT 100")
        admincomments = cursor.fetchall()
        cursor.close()
        return render_template("admin-comments.html", admincomments = admincomments)


@app.route('/admin/comments/delete/<int:id>', methods=("GET", "POST"))
@login_required
def deletecomment(id):
    if request.method == "POST":
        cursor = db.mysql.connection.cursor()
        deletestatement = "DELETE FROM pixelpost_comments where id = %s"
        cursor.execute(deletestatement,  (id,))
        db.mysql.connection.commit()
        cursor.close()

        return redirect(url_for("admincomments"))
    

@app.route('/admin/comments/publish/<int:id>', methods=("GET", "POST"))
@login_required
def publishcomment(id):
    if request.method == "POST":
        cursor = db.mysql.connection.cursor()
        publishstatement = "UPDATE pixelpost_comments SET publish = 'yes' where id = %s"
        cursor.execute(publishstatement,  (id,))
        db.mysql.connection.commit()
        cursor.close()

        return redirect(url_for("admincomments"))


@app.route('/admin/bookmark/create', methods=['GET', 'POST'])
@login_required
def create_bookmark():
    if request.method == 'POST':
        # Get the bookmark URL and tags from the form data
        bookmarkurl = request.form['url']
        bookmarktags = request.form['tags']

        # Use Requests to get the URL title tag
        url = bookmarkurl
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        title = response.text.split('<title>')[1].split('</title>')[0]

        # Insert the bookmark into the MySQL table
        cursor = db.mysql.connection.cursor()
        sql = "INSERT INTO bookmarks (url, title, tags) VALUES (%s, %s, %s)"
        val = (bookmarkurl, title, bookmarktags)
        cursor.execute(sql, val)
        db.mysql.connection.commit()
        cursor.close()
        flash('Stored bookmark "{}"'.format(title))
        return redirect(url_for("create_bookmark"))
    else:
        return render_template('admin-bookmarks.html')
    

@app.route('/admin/checkin', methods=['GET', 'POST'])
@login_required
def create_checkin():
    if request.method == 'POST':
        checkinVenue = request.form['venue']
        checkinAddress = request.form['address']
        checkinDatetime = datetime.now()
        checkinId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) 

        cursor = db.mysql.connection.cursor()
        mysql_insert_query = "INSERT ignore INTO recently (external_id, event_date, name, type, address) VALUES (%s, %s, %s, %s, %s)"
        record = (checkinId, checkinDatetime, checkinVenue, "Swarm", checkinAddress)
        cursor.execute(mysql_insert_query, record)
        db.mysql.connection.commit()
        cursor.close()

        # Get the count of checkins for the venue
        cursor = db.mysql.connection.cursor()
        cursor.execute('SELECT count(*) as count FROM recently WHERE name = %s and address = %s', (checkinVenue, checkinAddress))
        checkinCount = cursor.fetchone()
        cursor.close()

        flash('Stored checkin to "{}" - You have checked in here {} times'.format(checkinVenue, checkinCount[0]))

        return redirect(url_for("create_checkin"))

    if request.method == 'GET':
        # query the last 30 checkins from the recently table to display on the page
        cursor = db.mysql.connection.cursor()
        cursor.execute('SELECT name, address, type FROM ( SELECT id, name, address, type  FROM recently  WHERE type = "Swarm"  ORDER BY id DESC LIMIT 60) subquery GROUP BY name, address, type')
        venues = cursor.fetchall()
        cursor.close()

    return render_template('admin-checkins.html', venues=venues)
    

@app.route('/admin/header', methods=['GET'])
@login_required
def admin_header():
    return render_template('admin-header.html', active_page='header')


@app.route('/admin/header/upload', methods=['POST'])
@login_required
def admin_header_upload():
    uploaded_file = request.files.get('file')
    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({'error': 'No file provided'}), 400
    images_dir = os.path.join(app.static_folder, 'images')
    temp_path = os.path.join(images_dir, 'header_upload_temp.jpg')
    uploaded_file.save(temp_path)
    return jsonify({'url': '/static/images/header_upload_temp.jpg'})


@app.route('/admin/header/save', methods=['POST'])
@login_required
def admin_header_save():
    data = request.get_json()
    try:
        x = int(data['x'])
        y = int(data['y'])
        w = int(data['width'])
        h = int(data['height'])
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid crop data'}), 400

    images_dir = os.path.join(app.static_folder, 'images')
    temp_path = os.path.join(images_dir, 'header_upload_temp.jpg')
    output_path = os.path.join(images_dir, 'header.jpg')

    if not os.path.exists(temp_path):
        return jsonify({'error': 'No uploaded image found'}), 400

    try:
        subprocess.run([
            'convert',
            temp_path,
            '-auto-orient',
            '-crop', f'{w}x{h}+{x}+{y}',
            '+repage',
            '-resize', '1320x180!',
            '-strip',
            '-quality', '85',
            output_path
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Image processing failed'}), 500

    os.remove(temp_path)
    return jsonify({'ok': True})


@app.route('/admin/checkin-search', methods=['GET'])
@login_required
def checkin_search():
    search_term = request.args.get('q', '')
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT name, address FROM recently WHERE name LIKE %s and type = 'swarm' GROUP by name, address ORDER BY MAX(event_date) DESC LIMIT 10", (f'%{search_term}%',))
    results = cursor.fetchall()
    cursor.close()
    rows = []
    csrf_token = generate_csrf()
    html = f"<div id='comments'><ul>"
    for row in results:
        html += f"<li><strong>{row[0]}</strong><br />"
        html += f"{row[1]}"
        html += f"<form action='/admin/checkin' method='post' style='text-align: right; color: #195ddd'>"
        html += f"<input type='hidden' name='csrf_token' value='{csrf_token}'>"
        html += f'''<input name='venue' class='form-control' id='venue' value="{row[0]}" type='hidden'>'''
        html += f"<input name='address' class='form-control'  id='address' value='{row[1]}' type='hidden'>"
        html += f"<input type='submit' value='Checkin Here '  style='border: none; background: none; padding: 0;' ></form></li>"
    html += f"</ul>"
    return jsonify(html)

