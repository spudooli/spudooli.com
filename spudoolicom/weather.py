from spudoolicom import app
from flask import render_template
import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

@app.route('/weather')
def weather():
    barometer = r.get("indoorPressure")
    barometer = barometer[0:-2]

    saturday = r.get("saturdayForecastWord")
    sunday = r.get("sundayForecastWord")
    todayforecast = r.get("todayForecast")
    tomorrowforecast = r.get("tomorrowForecast")
    todaymax = r.get("todayMax")
    todaymin = r.get("todayMin")
    tomorrowmax = r.get("tomorrowMax")
    tomorrowmin = r.get("tomorrowMin")

    if saturday == "Partly cloudy":
        saturdayicon = "<span class='fs1 climacon cloud sun' aria-hidden='true'></span>"
    if saturday == "Few showers":
        saturdayicon = "<span class='fs1 climacon showers sun' aria-hidden='true'></span>"
    if saturday == "Showers":
        saturdayicon = "<span class='fs1 climacon showers' aria-hidden='true'></span>"
    if saturday == "Rain":
        saturdayicon = "<span class='fs1 climacon rain' aria-hidden='true'></span>"
    if saturday == "Fine":
        saturdayicon = "<span class='fs1 climacon sun' aria-hidden='true'></span>"
    if saturday == "Cloudy":
        saturdayicon = "<span class='fs1 climacon cloud' aria-hidden='true'></span>"
    if saturday == "Wind rain":
        saturdayicon = "<span class='fs1 climacon wind cloud' aria-hidden='true'></span>"
    if saturday == "Drizzle":
        saturdayicon = "<span class='fs1 climacon drizzle' aria-hidden='true'></span>"
    if saturday == "Windy":
        saturdayicon = "<span class='fs1 climacon wind' aria-hidden='true'></span>"
    if saturday == "Thunder":
        saturdayicon = "<span class='fs1 climacon lightning' aria-hidden='true'></span>"

    if sunday == "Partly cloudy":
        sundayicon = "<span class='fs1 climacon cloud sun' aria-hidden='true'></span>"
    if sunday == "Few showers":
        sundayicon = "<span class='fs1 climacon showers sun' aria-hidden='true'></span>"
    if sunday == "Showers":
        sundayicon = "<span class='fs1 climacon showers' aria-hidden='true'></span>"
    if sunday == "Rain":
        sundayicon = "<span class='fs1 climacon rain' aria-hidden='true'></span>"
    if sunday == "Fine":
        sundayicon = "<span class='fs1 climacon sun' aria-hidden='true'></span>"
    if sunday == "Cloudy":
        sundayicon = "<span class='fs1 climacon cloud' aria-hidden='true'></span>"
    if sunday == "Wind rain":
        sundayicon = "<span class='fs1 climacon wind cloud' aria-hidden='true'></span>"
    if sunday == "Drizzle":
        sundayicon = "<span class='fs1 climacon drizzle' aria-hidden='true'></span>"
    if sunday == "Windy":
        sundayicon = "<span class='fs1 climacon wind' aria-hidden='true'></span>"
    if sunday == "Thunder":
        sundayicon = "<span class='fs1 climacon lightning' aria-hidden='true'></span>"


    pressuredirection = r.get("pressureDirection")
    if pressuredirection == "up":
        pressuredirectionicon= "<ion-icon name='arrow-up-outline'></ion-icon>"
    if pressuredirection == "upslowly":
        pressuredirectionicon= "<ion-icon name='arrow-up-outline'></ion-icon>"
    if pressuredirection == "upslowly-goodcoming":
        pressuredirectionicon= "<ion-icon name='arrow-up-outline'></ion-icon>"
    if pressuredirection == "downslowly":
        pressuredirectionicon= "<ion-icon name='arrow-down-outline'></ion-icon>"
    if pressuredirection == "down":
        pressuredirectionicon= "<ion-icon name='arrow-down-outline'></ion-icon>"
    if pressuredirection == "downslowly-nogoodcoming":
        pressuredirectionicon= "<ion-icon name='arrow-down-outline'></ion-icon>"
    if pressuredirection == "stable":
        pressuredirectionicon= "<ion-icon name='arrow-forward-outline'></ion-icon>"

    html = todayforecast + "<br>"
    html += "Max: " + todaymax + "&deg;  Min: " + todaymin + "&deg;<br><br>"
    html += "<div class='counter-title'>The Forecast for Tomorrow</div>"
    html +=  tomorrowforecast + "<br> Max: " +  tomorrowmax + "&deg;  Min: " + tomorrowmin + "&deg;<br>"


    return render_template('weather.html', barometer = barometer, pressuredirectionicon = pressuredirectionicon, html = html,
                            saturdayicon = saturdayicon, sundayicon = sundayicon)
    

