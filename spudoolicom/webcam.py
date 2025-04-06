from spudoolicom import app
from flask import render_template, request, redirect
import requests
import os

def dotherequeststhing(requesturl):
    try:
        requests.get(requesturl)
    except requests.exceptions.RequestException as e: 
        print(e)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


@app.route('/webcam', strict_slashes=False)
def webcamindex():
    
    return redirect('/webcam/camera/kitchen', code=301)


@app.route('/webcam/camera/<camera>', strict_slashes=False)
def webcam(camera):
    if camera == "kitchen" or camera == "mancave" or camera == "driveway":
        print(camera)
    else:
        return redirect('/webcam/camera/kitchen', code=301)
    
    return render_template('webcam.html', camera = camera)

    
@app.route("/webcam/benchleds", methods=['POST'])
def benchleds():
    request_data = request.get_json()
    benchleds = request_data['onoroff']

    if benchleds == "on":
        #print("Setting colour to: " + benchleds)
        try:
            dotherequeststhing("http://192.168.1.142/benchleds-on")
        except:
            pass
    
    elif benchleds == "off":
        #print("Setting colour to: " + benchleds)
        try:
            dotherequeststhing("http://192.168.1.142/benchleds-off")
        except:
            pass

    return "ok"

@app.route("/webcam/mancaveleds", methods=['POST'])
def mancaveleds():
    request_data = request.get_json()
    mancaveleds = request_data['mancaveleds']

    mancaveleds = hex_to_rgb(mancaveleds)
    #print(str(mancaveleds))

    if mancaveleds:
        try:
           os.system("sudo -u dave /usr/local/bin/liquidctl --match Corsair set sync color clear")
           os.system("sudo -u dave /usr/local/bin/liquidctl --match Corsair set sync color fixed 'rgb" + str(mancaveleds) + "'")
           os.system("sudo -u dave /usr/local/bin/liquidctl --match Gigabyte set sync color fixed 'rgb" + str(mancaveleds) + "'")
        except:
            pass
    
    return "ok"
