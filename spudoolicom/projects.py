from flask import render_template, redirect
from spudoolicom import app, db
from datetime import date

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

    return render_template('projects.html', queenplaycount = queenplaycount, numTweetsToots = numTweetsToots)


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

    return render_template('too-much-queen.html', top20artists = top20artists, queenpercentage = queenpercentage, queenplaycount = queenplaycount, totalsongs = totalsongs)