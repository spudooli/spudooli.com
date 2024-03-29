from spudoolicom import app
from flask import render_template
import glob

@app.route('/house/charts/<where>')
def charts(where):
    if where == "indoor":
        pageHeading = "Indoor Temperatures"
        charts = sorted(glob.glob("spudoolicom/static/charts/inside*"))
    
    elif where == "outside":
        pageHeading = "Outdoor Temperatures"
        charts = sorted(glob.glob("spudoolicom/static/charts/outside*"))

    elif where == "kitchen":
        pageHeading = "Kitchen Temperatures and Humidity"
        charts = sorted(glob.glob("spudoolicom/static/charts/kitchen*"))

    elif where == "barometer":
        pageHeading = "Indoor Barometer h/Pa "
        charts = sorted(glob.glob("spudoolicom/static/charts/barometer*"))

    elif where == "mancave":
        pageHeading = "Mancave Temperature "
        charts = sorted(glob.glob("spudoolicom/static/charts/mancave*"))

    elif where == "shed":
        pageHeading = "Garden Shed Temperature "
        charts = sorted(glob.glob("spudoolicom/static/charts/shed*"))

    elif where == "power":
        pageHeading = "Electricity"
        charts = sorted(glob.glob("spudoolicom/static/charts/power*"))

    elif where == "heat":
        pageHeading = "Central Heating Output Temperature"
        charts = sorted(glob.glob("spudoolicom/static/charts/heat*"))

    elif where == "traegar":
        pageHeading = "Traeger Temperature"
        charts = glob.glob("spudoolicom/static/charts/traeger*")
    
    elif where == "spa":
        pageHeading = "Spa Pool"
        charts = glob.glob("spudoolicom/static/charts/spa*")
    
    elif where == "shed":
        pageHeading = "Garden Shed Temperatures"
        charts = glob.glob("spudoolicom/static/charts/shed*")
    
    else:
        pageHeading = "Nope"
        charts = ""
    
    return render_template('charts.html', charts = charts, pageHeading = pageHeading, where = where)
    

