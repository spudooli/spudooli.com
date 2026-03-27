from flask import render_template, redirect, request
from spudoolicom import app, db, cache
from datetime import date, datetime, timedelta
import os
import random


# Get the current year
current_year = datetime.now().year
# Create the date string for January 1st of the current year
year_start_date = f"{current_year}-01-01 00:00:01"


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
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT event_date, name, type, address, artist, album, external_id, url, item_image from recently WHERE name LIKE %s  AND type IN ('twitter', 'mastodon') ORDER by event_date ASC", (f'%{verse}%',))
    verse_data = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    verse = [dict(zip(column_names, row)) for row in verse_data]
    cursor.close()
    return verse

def catcount():
    # Get the count of cats
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM cats ")
    catcount = cursor.fetchone()
    catcount = "{:,}".format(catcount[0])
    return catcount

musicquery = """SELECT 
                DATE_FORMAT(months.month, '%Y-%m') AS this_month,
                COUNT(CASE WHEN r.artist IS NOT NULL THEN r.id ELSE NULL END) AS music
                FROM (
                SELECT 
                    LAST_DAY(DATE_ADD('2008-09-01', INTERVAL seq MONTH)) + INTERVAL 1 DAY - INTERVAL 1 MONTH AS month
                FROM (
                    SELECT 
                        @seq := @seq + 1 AS seq
                    FROM 
                        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
                        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b,
                        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c,
                        (SELECT @seq := -1) seq_init
                ) seqs
                WHERE 
                    LAST_DAY(DATE_ADD('2008-09-01', INTERVAL seq MONTH)) + INTERVAL 1 DAY - INTERVAL 1 MONTH <= LAST_DAY(CURRENT_DATE)
                ) months
                LEFT JOIN 
                    recently r ON DATE_FORMAT(r.event_date, '%Y-%m') = DATE_FORMAT(months.month, '%Y-%m')
                    AND r.type = 'lastfm'
                GROUP BY 
                    this_month
                ORDER BY 
                    this_month ASC;"""

checkinquery = """SELECT 
                DATE_FORMAT(months.month, '%Y-%m') AS this_month,
                COUNT(CASE WHEN r.name IS NOT NULL THEN r.id ELSE NULL END) AS music
                FROM (
                SELECT 
                    LAST_DAY(DATE_ADD('2009-11-15', INTERVAL seq MONTH)) + INTERVAL 1 DAY - INTERVAL 1 MONTH AS month
                FROM (
                    SELECT 
                        @seq := @seq + 1 AS seq
                    FROM 
                        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
                        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b,
                        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c,
                        (SELECT @seq := -1) seq_init
                ) seqs
                WHERE 
                    LAST_DAY(DATE_ADD('2009-11-15', INTERVAL seq MONTH)) + INTERVAL 1 DAY - INTERVAL 1 MONTH <= LAST_DAY(CURRENT_DATE)
                ) months
                LEFT JOIN 
                    recently r ON DATE_FORMAT(r.event_date, '%Y-%m') = DATE_FORMAT(months.month, '%Y-%m')
                    AND r.type = 'swarm'
                GROUP BY 
                    this_month
                ORDER BY 
                    this_month ASC;"""

@app.route('/projects', strict_slashes=False)
def projects():
    # Songs by Queen count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where artist = 'Queen' or artist = 'Queen & David Bowie' or artist = 'George Michael & Queen' or artist = 'Queen & George Michael'")
    results = cur.fetchone()
    queenplaycount = "{:,}".format(results[0])
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

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'Swarm'")
    swarmcount = cursor.fetchone()
    swarmcount = "{:,}".format(swarmcount[0])

    return render_template('projects.html', queenplaycount = queenplaycount, numTweetsToots = numTweetsToots, bookmarkcount = bookmarkcount, lastfmcount = lastfmcount, catscount = catscount, swarmcount = swarmcount)


@app.route('/projects/the-book-of-dave', strict_slashes=False, defaults={'verse': None} )
@app.route('/projects/the-book-of-dave/<verse>')
def thebookofdave(verse):
        randomverses = ["martini", "daughter", "wine", "wife", "pants", "cat"]
        arandomverse = random.choice(randomverses)
        if verse is None:
            verse = get_the_verse(arandomverse)
        else:
            verse = get_the_verse(verse)

        return render_template('the-book-of-dave.html', verse = verse, randomverses = randomverses, arandomverse = arandomverse)


@app.route('/projects/the-book-of-dave/search', methods=['GET'])
def thebookofdavesearch():
        query = request.args.get('query', '')
        if query:
            verse = get_the_verse(query)
            return render_template('the-book-of-dave.html', verse = verse, query = query)


@app.route('/projects/too-much-queen', strict_slashes=False)
@cache.cached(timeout=7200)
def toomuchqueen():
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen where artist = 'Queen' or artist = 'Queen & David Bowie' or artist = 'George Michael & Queen' or artist = 'Queen & George Michael'")
    results = cur.fetchone()
    queenplaycount = results[0]
    cur.close()  
    
    top20artists = gettop20artists()
    top20songs = gettop20songs()

    haurakisongcount = 0
    thesoundsongcount = 0
    thecoastsongcount = 0
    goldfmsongcount = 0
    channelxsongcount = 0

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT station, COUNT(*) FROM too_much_queen GROUP BY station")
    station_counts = cur.fetchall()
    cur.close()

    for station, count in station_counts:
        if station == 'hauraki':
            haurakisongcount = count
        elif station == 'thesound':
            thesoundsongcount = count
        elif station == 'thecoast':
            thecoastsongcount = count
        elif station == 'goldfm':
            goldfmsongcount = count
        elif station == 'channelx':
            channelxsongcount = count

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) FROM too_much_queen")
    results = cur.fetchone()
    totalsongcount = results[0]
    cur.close()

    queenpercentage = round((queenplaycount / totalsongcount) * 100, 2)
    
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

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) as playcount, artist, song_name from too_much_queen where station = 'channelx' group by song_name, artist order by playcount desc limit 20")
    cxsongs20 = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    channelxsongs20 = [dict(zip(column_names, row)) for row in cxsongs20]
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

    cursor = db.mysql.connection.cursor()
    cursor.execute("""
        SELECT station, ROUND(AVG(monthly_unique)) as avg_unique_per_month
        FROM (
            SELECT station,
                   DATE_FORMAT(played_date, '%Y-%m') as month,
                   COUNT(DISTINCT artist) as monthly_unique
            FROM too_much_queen
            GROUP BY station, month
        ) monthly_counts
        GROUP BY station
        ORDER BY avg_unique_per_month DESC
    """)
    avgstation = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    avguniqueartistsbystation = [dict(zip(column_names, row)) for row in avgstation]
    cursor.close()

      # Get all months spend for KFC
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM played_date) thismonth, COUNT(*) AS play_count FROM too_much_queen where artist = 'Queen' or artist = 'Queen & David Bowie' or artist = 'George Michael & Queen' or artist = 'Queen & George Michael' GROUP BY thismonth ORDER BY thismonth ASC")
    queenplaysbymonth = cur.fetchall()
    queenplaysbymonthlabels = [row[0] for row in queenplaysbymonth]
    queenplaysbymonthvalues = [str(row[1]).replace("-","") for row in queenplaysbymonth]
    cur.close() 

    return render_template('too-much-queen.html', top20artists = top20artists, queenpercentage = queenpercentage, queenplaycount = queenplaycount,
                           top20songs = top20songs, haurakisongcount = haurakisongcount, thesoundsongcount = thesoundsongcount,
                           thecoastsongcount = thecoastsongcount, goldfmsongcount = goldfmsongcount, channelxsongcount = channelxsongcount,
                           totalsongcount = totalsongcount, haurakisongs20 = haurakisongs20,
                           thesoundsongs20 = hthesoundsongs20, artistsbystation = artistsbystation, distinctartists = distinctartists, thecoastsongs20 = thecoastsongs20,
                           channelxsongs20 = channelxsongs20,
                           queenplaysbymonthlabels = queenplaysbymonthlabels, queenplaysbymonthvalues = queenplaysbymonthvalues,
                           avguniqueartistsbystation = avguniqueartistsbystation)


@app.route('/projects/bookmarks', defaults={'tag_filter': None})
@app.route('/projects/bookmarks/<tag_filter>')
def bookmarks(tag_filter):

    cur = db.mysql.connection.cursor()
    cur.execute("SELECT id, url, title, tags FROM bookmarks ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()

    all_bookmarks = [{'id': r[0], 'url': r[1], 'title': r[2], 'tags': r[3]} for r in rows]

    tag_counts = {}
    for b in all_bookmarks:
        if b['tags']:
            for tag in [t.strip() for t in b['tags'].split(',')]:
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    popular_tags = sorted(tag for tag, count in tag_counts.items() if count >= 2)

    if tag_filter:
        displayed = [b for b in all_bookmarks if b['tags'] and tag_filter in [t.strip() for t in b['tags'].split(',')]]
    else:
        displayed = all_bookmarks

    return render_template('bookmarks.html', bookmarks=displayed, bookmarkcount=len(all_bookmarks), popular_tags=popular_tags, active_tag=tag_filter)


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
    cursor.execute("SELECT count(artist) as playcount, artist from recently where type = 'LastFM' group by artist ORDER BY playcount DESC LIMIT 40")
    top40 = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    top40artists = [dict(zip(column_names, row))
                for row in top40]
    
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `recently` WHERE `name` LIKE '%Life Is a Rollercoaster%'")
    rollercoaster = cursor.fetchone()
    rollercoaster = "{:,}".format(rollercoaster[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(name) as playcount, name, artist from recently where type = 'LastFM' group by name, artist ORDER BY playcount DESC LIMIT 40")
    top40songs = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    top40songsplayed = [dict(zip(column_names, row))
                for row in top40songs]
    
    ###### Stats for this year ######
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(name) as playcount, name, artist from recently where type = 'LastFM' and event_date > %s group by name, artist ORDER BY playcount DESC LIMIT 40", (year_start_date,))
    top40songsyear = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    top40songsplayedyear = [dict(zip(column_names, row))
                for row in top40songsyear]\
                
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(artist) as playcount, artist from recently where type = 'LastFM' and event_date > %s group by artist ORDER BY playcount DESC LIMIT 40", (year_start_date,))
    top40_year = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    top40artistsyear = [dict(zip(column_names, row))
                for row in top40_year]
    
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'LastFM' and event_date > %s", (year_start_date,))
    lastfmcountyear = cursor.fetchone()
    lastfmcountyear = "{:,}".format(lastfmcountyear[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(DISTINCT artist) FROM recently where type = 'LastFM' and event_date > %s", (year_start_date,))
    artistcountyear = cursor.fetchone()
    artistcountyear = "{:,}".format(artistcountyear[0])
    
    # Get all months music by month
    cur = db.mysql.connection.cursor()
    cur.execute(musicquery)
    playsbymonth = cur.fetchall()
    playsbymonthlabels = [row[0] for row in playsbymonth]
    playsbymonthvalues = [str(row[1]).replace("-","") for row in playsbymonth]
    cur.close() 


    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) FROM `recently` WHERE `artist` LIKE '%Public Image%'")
    publicimage = cursor.fetchone()
    publicimage = "{:,}".format(publicimage[0])

    # Build GitHub-style activity heatmap for last 52 weeks
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    current_week_sunday = today - timedelta(days=days_since_sunday)
    heatmap_start = current_week_sunday - timedelta(weeks=51)

    cursor = db.mysql.connection.cursor()
    cursor.execute("""
        SELECT DATE(event_date) as play_date, COUNT(*) as cnt
        FROM recently
        WHERE type = 'LastFM'
        AND event_date >= %s
        GROUP BY DATE(event_date)
    """, (heatmap_start,))
    daily_rows = cursor.fetchall()
    music_by_day = {str(row[0]): row[1] for row in daily_rows}

    def count_to_level(n):
        if n == 0: return 0
        if n == 1: return 1
        if n <= 3: return 2
        if n <= 6: return 3
        return 4

    music_weeks = []
    music_week_month_labels = []
    for week_idx in range(52):
        week_start = heatmap_start + timedelta(weeks=week_idx)
        if week_idx == 0:
            music_week_month_labels.append(week_start.strftime('%b'))
        else:
            prev_start = heatmap_start + timedelta(weeks=week_idx - 1)
            music_week_month_labels.append(week_start.strftime('%b') if week_start.month != prev_start.month else '')
        week = []
        for day_offset in range(7):
            d = week_start + timedelta(days=day_offset)
            date_str = d.strftime('%Y-%m-%d')
            count = music_by_day.get(date_str, 0)
            is_future = d > today
            week.append({
                'date': date_str,
                'count': count,
                'level': 0 if is_future else count_to_level(count),
                'future': is_future,
            })
        music_weeks.append(week)

    return render_template('music.html', lastfmcount = lastfmcount, artistcount = artistcount, top40artists = top40artists, rollercoaster = rollercoaster,
                           top40songsplayed = top40songsplayed, publicimage = publicimage, playsbymonthlabels = playsbymonthlabels,
                           playsbymonthvalues = playsbymonthvalues, top40songsplayedyear = top40songsplayedyear, top40artistsyear = top40artistsyear,
                           lastfmcountyear = lastfmcountyear, artistcountyear = artistcountyear,
                           music_weeks = music_weeks, music_week_month_labels = music_week_month_labels)


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

@app.route('/projects/checkins')
def checkins():

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(id) id FROM recently where type = 'swarm'")
    swarmcount = cursor.fetchone()
    swarmcount = "{:,}".format(swarmcount[0])

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(name) as checkincount, name, address from recently where type = 'swarm' group by name,address ORDER BY checkincount DESC LIMIT 40")
    topcheckins = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    topcheckinsplaces = [dict(zip(column_names, row))
                for row in topcheckins]

    # Count of unique locations checked in to
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT count(DISTINCT name, IFNULL(address, '')) as checkincount FROM recently where type = 'swarm'")
    uniquecheckins = cursor.fetchone()
    uniquecheckins = "{:,}".format(uniquecheckins[0])

    cur = db.mysql.connection.cursor()
    cur.execute(checkinquery)
    placesbymonth = cur.fetchall()
    placesbymonthlabels = [row[0] for row in placesbymonth]
    placesbymonthvalues = [str(row[1]).replace("-","") for row in placesbymonth]
    cur.close()

    # Build GitHub-style activity heatmap for last 52 weeks
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    current_week_sunday = today - timedelta(days=days_since_sunday)
    heatmap_start = current_week_sunday - timedelta(weeks=51)

    cursor = db.mysql.connection.cursor()
    cursor.execute("""
        SELECT DATE(event_date) as checkin_date, COUNT(*) as cnt
        FROM recently
        WHERE type = 'swarm'
        AND event_date >= %s
        GROUP BY DATE(event_date)
    """, (heatmap_start,))
    daily_rows = cursor.fetchall()
    checkins_by_day = {str(row[0]): row[1] for row in daily_rows}

    def count_to_level(n):
        if n == 0: return 0
        if n == 1: return 1
        if n <= 3: return 2
        if n <= 6: return 3
        return 4

    checkins_weeks = []
    week_month_labels = []
    for week_idx in range(52):
        week_start = heatmap_start + timedelta(weeks=week_idx)
        if week_idx == 0:
            week_month_labels.append(week_start.strftime('%b'))
        else:
            prev_start = heatmap_start + timedelta(weeks=week_idx - 1)
            week_month_labels.append(week_start.strftime('%b') if week_start.month != prev_start.month else '')
        week = []
        for day_offset in range(7):
            d = week_start + timedelta(days=day_offset)
            date_str = d.strftime('%Y-%m-%d')
            count = checkins_by_day.get(date_str, 0)
            is_future = d > today
            week.append({
                'date': date_str,
                'count': count,
                'level': 0 if is_future else count_to_level(count),
                'future': is_future,
            })
        checkins_weeks.append(week)

    return render_template('checkins.html', swarmcount = swarmcount, topcheckinsplaces = topcheckinsplaces, placesbymonthlabels = placesbymonthlabels, placesbymonthvalues = placesbymonthvalues, uniquecheckins = uniquecheckins, checkins_weeks = checkins_weeks, week_month_labels = week_month_labels)