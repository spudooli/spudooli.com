from flask import render_template, redirect
from spudoolicom import app, db
from datetime import date
import os

def gettop20artists():
    # Get the top 20 artists
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) as playcount, artist from too_much_queen group by artist order by playcount desc limit 20")
    top20artists = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    artists20 = [dict(zip(column_names, row))
                for row in top20artists]
    cursor.close()
    return artists20

def gettop20songs():
    # Get the top 20 songs
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) as playcount, artist, song_name from too_much_queen group by song_name, artist order by playcount desc limit 20")
    top20songs = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    songs20 = [dict(zip(column_names, row))
                for row in top20songs]
    cursor.close()
    return songs20

def getbookmarkcount():
    #get the count of bookmarks
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM bookmarks")
    bookmarkcount = cur.fetchone()
    bookmarkcount = "{:,}".format(bookmarkcount[0])
    cur.close()

    return bookmarkcount

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

@app.route('/projects', strict_slashes=False)
def projects():
    # Songs by Queen count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where artist like '%Queen%' and artist not like 'Queensryche' and artist not like 'Queens of the Stone Age'")
    results = cur.fetchone()
    queenplaycount = results[0]
    cur.close()  

    # get to total tweets and toots from the database
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM recently where type like 'Twitter' or type like 'Mastodon'")
    numTweetsToots = cur.fetchone()
    numTweetsToots = "{:,}".format(numTweetsToots[0])
    cur.close()

    bookmarkcount = getbookmarkcount()

    return render_template('projects.html', queenplaycount = queenplaycount, numTweetsToots = numTweetsToots, bookmarkcount = bookmarkcount)


@app.route('/projects/the-book-of-dave', strict_slashes=False)
def thebookofdave():

    return render_template('the-book-of-dave.html', )


@app.route('/projects/too-much-queen', strict_slashes=False)
def toomuchqueen():

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where artist like '%Queen%' and artist not like 'Queensryche' and artist not like 'Queens of the Stone Age'")
    results = cur.fetchone()
    queenplaycount = results[0]
    cur.close()  

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen")
    results = cur.fetchone()
    totalsongs = results[0]
    cur.close() 

    queenpercentage = round((queenplaycount / totalsongs) * 100, 2)

    top20artists = gettop20artists()
    top20songs = gettop20songs()

    return render_template('too-much-queen.html', top20artists = top20artists, queenpercentage = queenpercentage, queenplaycount = queenplaycount, totalsongs = totalsongs, top20songs = top20songs)


@app.route('/projects/bookmarks')
def bookmarks():
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT * FROM bookmarks")
    bookmarks = cur.fetchall()
    cur.close()

    bookmarkcount = getbookmarkcount()

    return render_template('bookmarks.html', bookmarks = bookmarks, bookmarkcount = bookmarkcount)


@app.route('/projects/spudpic')
def spudpic():

    image_dir = '/var/www/spudooli/spudoolicom/static/images/spudpic/'
    files_by_creation_date = list_files_by_creation_date(image_dir)

    image_files = [f for f in files_by_creation_date]  

    return render_template('spudpic.html', image_files = image_files)