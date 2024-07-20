from flask import render_template
from spudoolicom import app, db
from datetime import datetime


@app.route('/money')
def money():
    
    # get number of transactions from the database
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) id FROM  `budget`")
    numTransactions = cur.fetchone()
    numTransactions = "{:,}".format(numTransactions[0])
    cur.close()

    # Get the date of the last transaction
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT date FROM  `budget` order by date desc limit 1")
    lastTransaction = cur.fetchone()
    lastTransaction = lastTransaction[0]
    cur.close()
    date_obj = datetime.strptime(str(lastTransaction), "%Y-%m-%d")
    lastTransaction = date_obj.strftime("%d/%m/%Y")

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

     # Get Gull petrol purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE `category` LIKE 'petrol' AND `party` LIKE 'gull%'")
    gull = cur.fetchone()
    gull = "{:,}".format(gull[0])
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
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) thismonth, SUM(case when category = 'Petrol' then amount else 0 end) as warehouse FROM budget GROUP BY thismonth order by thismonth asc")
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
    cur.execute("SELECT sum(amount) amount FROM `budget` WHERE category = 'The Warehouse'")
    totalWarehouseSpend = cur.fetchone()
    totalWarehouseSpend = "{:,}".format(totalWarehouseSpend[0])
    cur.close()

    # Get all months spend for The Warehouse
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) thismonth, SUM(case when category = 'The Warehouse' then amount else 0 end) as warehouse FROM budget GROUP BY thismonth order by thismonth asc")
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

         # Get Bunnings Constellation purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT count(id) id FROM  `budget` WHERE  `party` LIKE  '%9470%'")
    bunningsconstellation = cur.fetchone()
    bunningsconstellation = "{:,}".format(bunningsconstellation[0])
    cur.close()

    # Get all months spend for Hardware
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) thismonth, SUM(case when category LIKE '%Hardware%' then amount else 0 end) as hardware FROM budget GROUP BY thismonth order by thismonth asc")
    data = cur.fetchall()
    hardwarelabels = [row[0] for row in data]
    hardwarevalues = [str(row[1]).replace("-","") for row in data]
    cur.close() 

    # Get KFC purchases
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT SUM( amount ) amount FROM  `budget` WHERE  `party` LIKE  '%kfc%'")
    kfctotal = cur.fetchone()
    kfctotal = "{:,}".format(kfctotal[0])
    cur.close()

    # Get all months spend for KFC
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT EXTRACT(Year_MONTH FROM date) thismonth, SUM(case when party LIKE '%kfc%' then amount else 0 end) as kfc FROM budget GROUP BY thismonth order by thismonth asc")
    kfcdata = cur.fetchall()
    kfclabels = [row[0] for row in data]
    kfcvalues = [str(row[1]).replace("-","") for row in kfcdata]
    cur.close() 
    
    return render_template('money.html', totalPetrolSpend = totalPetrolSpend, warehouselabels = warehouselabels, numTransactions = numTransactions,
                          totalWarehouseSpend = totalWarehouseSpend, warehousevalues = warehousevalues, farro = farro, lastTransaction = lastTransaction,
                          paknsave = paknsave, newworld= newworld, countdown = countdown, shellZ = shellZ, caltex = caltex, 
                          bp = bp, mobil = mobil, labels = labels, values = values, totalSupermarketSpend = totalSupermarketSpend, 
                          hardwarelabels = hardwarelabels, hardwarevalues = hardwarevalues, hardware = hardware, bunningsconstellation = bunningsconstellation, 
                          gull = gull, kfctotal = kfctotal, kfclabels = kfclabels, kfcvalues = kfcvalues)

                          
