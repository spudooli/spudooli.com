from spudoolicom import app, db
from flask import render_template

@app.route('/money')
def money():

     # Get all petrol purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `category` LIKE  'petrol'")
    totalPetrolSpend = cur.fetchone()
    totalPetrolSpend = "{:,}".format(totalPetrolSpend[0])
    cur.close()        

     # Get Shell/Z petrol purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE `category` LIKE 'petrol' AND `party` LIKE '%shell%' OR party like 'Z %'")
    shellZ = cur.fetchone()
    shellZ = "{:,}".format(shellZ[0])
    cur.close()   

     # Get Caltex petrol purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE `category` LIKE 'petrol' AND `party` LIKE '%caltex%'")
    caltex = cur.fetchone()
    caltex = "{:,}".format(caltex[0])
    cur.close()  

     # Get BP petrol purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE `category` LIKE 'petrol' AND `party` LIKE '%bp%'")
    bp = cur.fetchone()
    bp = "{:,}".format(bp[0])
    cur.close()  

     # Get BP petrol purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE `category` LIKE 'petrol' AND `party` LIKE '%mobil%'")
    mobil = cur.fetchone()
    mobil = "{:,}".format(mobil[0])
    cur.close()  

    # Get all months spent on petrol
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) newdate, sum(amount) amount FROM `budget` WHERE `category` LIKE 'petrol' GROUP BY newdate")
    data = cur.fetchall()
    labels = [row[0] for row in data]
    values = [str(row[1]).replace("-","") for row in data]
    cur.close()  

     # Get all supermarket purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `category` LIKE  'supermarket'  or category like '%small%'")
    totalSupermarketSpend = cur.fetchone()
    totalSupermarketSpend = "{:,}".format(totalSupermarketSpend[0])
    cur.close()     

    # Get Countdown supermarket purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `party` LIKE  '%countdown%'  or party like '%foodtown%' or party like '%woolworths%'")
    countdown = cur.fetchone()
    countdown = "{:,}".format(countdown[0])
    cur.close()    

    # Get Countdown supermarket purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `party` LIKE  '%new world%'")
    newworld = cur.fetchone()
    newworld = "{:,}".format(newworld[0])
    cur.close()

    # Get Countdown supermarket purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `party` LIKE  '%pak%'")
    paknsave = cur.fetchone()
    paknsave = "{:,}".format(paknsave[0])
    cur.close()

    # Get Countdown supermarket purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `party` LIKE  '%farro%'")
    farro = cur.fetchone()
    farro = "{:,}".format(farro[0])
    cur.close()

    return render_template('money.html', totalPetrolSpend = totalPetrolSpend, farro = farro, paknsave = paknsave, newworld= newworld, countdown = countdown, shellZ = shellZ, caltex = caltex, bp = bp, mobil = mobil, labels = labels, values = values, totalSupermarketSpend = totalSupermarketSpend)