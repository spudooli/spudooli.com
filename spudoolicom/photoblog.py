from spudoolicom import app, db
from flask import render_template


@app.route('/photoblog')
def photoblog():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image FROM pixelpost_pixelpost ORDER BY id DESC LIMIT 10")
    posts = cursor.fetchall()
    cursor.close()
    return render_template('photoblog.html', posts = posts)


@app.route('/photoblog/<id>')
def post(id):
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, image, body FROM pixelpost_pixelpost where id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, parent_id, message, name FROM pixelpost_comments where parent_id = %s", (id,))
    comments = cursor.fetchall()
    cursor.close()
    return render_template('post.html', post = post, comments = comments)

