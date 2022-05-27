from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from spudoolicom import app, db
import os
from werkzeug.utils import secure_filename
from datetime import datetime


@app.route("/admin/create", methods=("GET", "POST"))
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
def adminposts():
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id, headline, body, image, alt_body, datetime, FROM pixelpost_pixelpost order by id DESC LIMIT 100")
        adminposts = cursor.fetchall()
        cursor.close()
        return render_template("admin-posts.html", adminposts = adminposts)


@app.route('/admin/comments')
def admincomments():
        cursor = db.mysql.connection.cursor()
        cursor.execute("SELECT id, parent_id, datetime, message, name, url, publish FROM pixelpost_comments order by id DESC LIMIT 100")
        admincomments = cursor.fetchall()
        cursor.close()
        return render_template("admin-comments.html", admincomments = admincomments)

@app.route('/admin/comments/delete/<int:id>', methods=("GET", "POST"))
def deletecomment(id):
    if request.method == "POST":
        cursor = db.mysql.connection.cursor()
        deletestatement = "DELETE FROM pixelpost_comments where id = %s"
        cursor.execute(deletestatement,  (id,))
        db.mysql.connection.commit()
        cursor.close()

        return redirect(url_for("admincomments"))

@app.route('/admin/comments/publish/<int:id>', methods=("GET", "POST"))
def publishcomment(id):
    if request.method == "POST":
        cursor = db.mysql.connection.cursor()
        publishstatement = "UPDATE pixelpost_comments SET publish = 'yes' where id = %s"
        cursor.execute(publishstatement,  (id,))
        db.mysql.connection.commit()
        cursor.close()

        return redirect(url_for("admincomments"))




# @app.route("/admin/<int:id>/update", methods=("GET", "POST"))
# def update(id):
#     """Update a post if the current user is the author."""
#     post = get_post(id)

#     if request.method == "POST":
#         title = request.form["title"]
#         body = request.form["body"]
#         error = None

#         if not title:
#             error = "Title is required."

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for("photoblog.index"))

#    return render_template("photoblog/update.html", post=post)

# @app.route('/admin/delete/<int:id>', methods=('POST',))
# def delete(id):
#     cur = db.mysql.connection.cursor()
#     cur.execute('DELETE FROM pixelpost_pixelpost WHERE id = ?', (id))
#     db.mysql.connection.commit()
#     cur.close()
#     return redirect(url_for('photoblog'))