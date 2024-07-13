from flask import render_template, redirect
from spudoolicom import app, db
from datetime import date
import os
import random

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

def get_the_verse(verse):
    # Get the verse
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT verse from the_book_of_dave where verse = %s", (verse,))
    verse = cursor.fetchall()
    column_names = [col[0] for col in verse]
    verse = [dict(zip(column_names, row))
                for row in verse]
    cursor.close()
    return verse

def catcount():
    # Get the count of cats
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM cats ")
    catcount = cursor.fetchone()
    catcount = "{:,}".format(catcount[0])
    return catcount

@app.route('/projects', strict_slashes=False)
def projects():
    # Songs by Queen count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where artist like '%Queen%' and artist not like 'Queensryche' and artist not like 'Queens of the Stone Age'and artist not like 'Bling Queen'")
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
    catscount = catcount()

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'LastFM'")
    lastfmcount = cursor.fetchone()
    lastfmcount = "{:,}".format(lastfmcount[0])

    return render_template('projects.html', queenplaycount = queenplaycount, numTweetsToots = numTweetsToots, bookmarkcount = bookmarkcount, lastfmcount = lastfmcount, catscount = catscount)


@app.route('/projects/the-book-of-dave/<verse>', strict_slashes=False)
def thebookofdave(verse):
    # If the verse  is not in the URL then select a random verse from an array
    if verse is None:
        verses = ["martini", "daughter", "wine", "wife", "pants"]
        get_the_verse(random.choice(verses))


    




    return render_template('the-book-of-dave.html', verse = verse)


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

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where station = 'hauraki'")
    results = cur.fetchone()
    haurakisongcount = results[0]
    cur.close()  

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where station = 'thesound'")
    results = cur.fetchone()
    thesoundsongcount = results[0]
    cur.close() 

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where station = 'thecoast'")
    results = cur.fetchone()
    thecoastsongcount = results[0]
    cur.close()  

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where station = 'goldfm'")
    results = cur.fetchone()
    goldfmsongcount = results[0]
    cur.close()  

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen")
    results = cur.fetchone()
    totalsongcount = results[0]
    cur.close()    

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) as playcount, artist, song_name from too_much_queen where station = 'hauraki' group by song_name, artist order by playcount desc limit 20")
    hsongs20 = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    haurakisongs20 = [dict(zip(column_names, row))
                for row in hsongs20]
    cursor.close()

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) as playcount, artist, song_name from too_much_queen where station = 'thesound' group by song_name, artist order by playcount desc limit 20")
    tssongs20 = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    hthesoundsongs20 = [dict(zip(column_names, row))
                for row in tssongs20]
    cursor.close()

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) as playcount, artist, song_name from too_much_queen where station = 'thecoast' group by song_name, artist order by playcount desc limit 20")
    tcsongs20 = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    thecoastsongs20 = [dict(zip(column_names, row))
                for row in tcsongs20]
    cursor.close()

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(distinct artist) FROM too_much_queen")
    results = cur.fetchone()
    distinctartists = results[0]
    cur.close()    

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count( distinct artist) as artistplaycount, station from too_much_queen  group by station")
    artistsstation = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    artistsbystation = [dict(zip(column_names, row))
                for row in artistsstation]
    cursor.close()

    return render_template('too-much-queen.html', top20artists = top20artists, queenpercentage = queenpercentage, queenplaycount = queenplaycount, 
                           totalsongs = totalsongs, top20songs = top20songs, haurakisongcount = haurakisongcount, thesoundsongcount = thesoundsongcount, 
                           thecoastsongcount = thecoastsongcount, goldfmsongcount = goldfmsongcount, totalsongcount = totalsongcount, haurakisongs20 = haurakisongs20, 
                           thesoundsongs20 = hthesoundsongs20, artistsbystation = artistsbystation, distinctartists = distinctartists, thecoastsongs20 = thecoastsongs20)


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


@app.route('/projects/music')
def music():

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'LastFM'")
    lastfmcount = cursor.fetchone()
    lastfmcount = "{:,}".format(lastfmcount[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(DISTINCT artist) FROM recently where type = 'LastFM'")
    artistcount = cursor.fetchone()
    artistcount = "{:,}".format(artistcount[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(artist) as playcount, artist from recently where type = 'LastFM' group by artist ORDER BY playcount DESC LIMIT 30")
    top30 = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    top30artists = [dict(zip(column_names, row))
                for row in top30]
    
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `recently` WHERE `name` LIKE '%Life Is a Rollercoaster%'")
    rollercoaster = cursor.fetchone()
    rollercoaster = "{:,}".format(rollercoaster[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(name) as playcount, name, artist from recently where type = 'LastFM' group by name, artist ORDER BY playcount DESC LIMIT 30")
    top30songs = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    top30songsplayed = [dict(zip(column_names, row))
                for row in top30songs]
    
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `recently` WHERE `artist` LIKE '%Public Image%'")
    publicimage = cursor.fetchone()
    publicimage = "{:,}".format(publicimage[0])

    return render_template('music.html', lastfmcount = lastfmcount, artistcount = artistcount, top30artists = top30artists, rollercoaster = rollercoaster, 
                           top30songsplayed = top30songsplayed, publicimage = publicimage)


@app.route('/projects/cats')
def cats():
    catscount = catcount()

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, cateventid, created_at FROM cats order by id desc limit 5")
    last3cats = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    latest3cats = [dict(zip(column_names, row))
                for row in last3cats]

    return render_template('cats.html', catscount = catscount, latest3cats = latest3cats)
