from flask import render_template
from spudoolicom import app, db

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

    # Get The Warehouse purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE `party` LIKE '%thl%' or party like '%the warehouse%'")
    totalWarehouseSpend = cur.fetchone()
    totalWarehouseSpend = "{:,}".format(totalWarehouseSpend[0])
    cur.close()

    # Get all months spend for The Warehouse
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) thismonth, SUM(case when party LIKE '%the warehouse%' or party like '%twh%' then amount else 0 end) as warehouse FROM budget GROUP BY thismonth")
    data = cur.fetchall()
    warehouselabels = [row[0] for row in data]
    warehousevalues = [str(row[1]).replace("-","") for row in data]
    cur.close() 

     # Get Hardwaretotal purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `category` LIKE  '%Hardware%'")
    hardware = cur.fetchone()
    hardware = "{:,}".format(hardware[0])
    cur.close()

         # Get Bunnings Censtellation purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) id FROM  `budget` WHERE  `party` LIKE  '%9470%'")
    bunningsconstellation = cur.fetchone()
    bunningsconstellation = "{:,}".format(bunningsconstellation[0])
    cur.close()

    # Get all months spend for Hardware
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) thismonth, SUM(case when category LIKE '%Hardware%' then amount else 0 end) as hardware FROM budget GROUP BY thismonth")
    data = cur.fetchall()
    hardwarelabels = [row[0] for row in data]
    hardwarevalues = [str(row[1]).replace("-","") for row in data]
    cur.close() 
    
    return render_template('money.html', totalPetrolSpend = totalPetrolSpend, warehouselabels = warehouselabels, 
                          totalWarehouseSpend = totalWarehouseSpend, warehousevalues = warehousevalues, farro = farro, 
                          paknsave = paknsave, newworld= newworld, countdown = countdown, shellZ = shellZ, caltex = caltex, 
                          bp = bp, mobil = mobil, labels = labels, values = values, totalSupermarketSpend = totalSupermarketSpend, 
                          hardwarelabels = hardwarelabels, hardwarevalues = hardwarevalues, hardware = hardware, bunningsconstellation = bunningsconstellation)

                          
