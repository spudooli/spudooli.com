from email.mime import image
from spudoolicom import app, db
from flask import render_template
import glob

@app.route('/house/charts/<where>')
def charts(where):
    if where == "indoor":
        pageHeading = "Indoor Temperatures"
        charts = sorted(glob.glob("spudoolicom/static/charts/inside*"))
    
    if where == "outside":
        pageHeading = "Outdoor Temperatures"
        charts = sorted(glob.glob("spudoolicom/static/charts/outside*"))

    if where == "kitchen":
        pageHeading = "Kitchen Temperatures"
        charts = sorted(glob.glob("spudoolicom/static/charts/kitchen*"))

    if where == "barometer":
        pageHeading = "Indoor Barometer h/Pa "
        charts = sorted(glob.glob("spudoolicom/static/charts/barometer*"))

    if where == "mancave":
        pageHeading = "Mancave Temperature "
        charts = sorted(glob.glob("spudoolicom/static/charts/mancave*"))

    if where == "shed":
        pageHeading = "Garden Shed Temperature "
        charts = sorted(glob.glob("spudoolicom/static/charts/shed*"))

    if where == "power":
        pageHeading = "Electricity"
        charts = sorted(glob.glob("spudoolicom/static/charts/power*"))

    if where == "heat":
        pageHeading = "Central Heating Output Temperature"
        charts = sorted(glob.glob("spudoolicom/static/charts/heat*"))

    if where == "traegar":
        pageHeading = "Traegar Temperature"
        charts = glob.glob("spudoolicom/static/charts/traegar*")
    
    return render_template('charts.html', charts = charts, pageHeading = pageHeading)
    

