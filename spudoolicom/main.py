from spudoolicom import app
from flask import render_template


@app.route('/')
def main():

    #Return the number of photos
    f = open("/var/www/scripts/power.txt", "r")    
    power = f.read()
    power = power.split(",")[0]

    # return the bank balance
    f = open("/var/www/scripts/otherbalance.txt", "r")    
    bankbalance = f.read()
    bankbalance = "$" + bankbalance.split(".")[0]


    return render_template('index.html', bankbalance = bankbalance, power = power)