from spudoolicom import app
from flask import render_template, request
import requests

def dotherequeststhing(requesturl):
    try:
        requests.get(requesturl)
    except requests.exceptions.RequestException as e: 
        print(e)


@app.route('/webcam')
def webcam():


    return render_template('webcam.html', )

    
@app.route("/webcam/benchleds", methods=['POST'])
def benchleds():
    request_data = request.get_json()
    benchleds = request_data['onoroff']

    if benchleds == "on":

        print("Setting colour to: " + benchleds)

        try:
            dotherequeststhing("http://192.168.1.142/benchleds-on")
        except:
            pass
    
    elif benchleds == "off":
            
        print("Setting colour to: " + benchleds)
    
        try:
            dotherequeststhing("http://192.168.1.142/benchleds-off")
        except:
            pass

    return "ok"
