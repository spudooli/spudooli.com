from spudoolicom import app
from flask import render_template
import redis

r = redis.from_url(app.config['REDIS_URL'], encoding="utf-8", decode_responses=True)

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
    elif saturday == "Few showers":
        saturdayicon = "<span class='fs1 climacon showers sun' aria-hidden='true'></span>"
    elif saturday == "Showers":
        saturdayicon = "<span class='fs1 climacon showers' aria-hidden='true'></span>"
    elif saturday == "Rain":
        saturdayicon = "<span class='fs1 climacon rain' aria-hidden='true'></span>"
    elif saturday == "Fine":
        saturdayicon = "<span class='fs1 climacon sun' aria-hidden='true'></span>"
    elif saturday == "Cloudy":
        saturdayicon = "<span class='fs1 climacon cloud' aria-hidden='true'></span>"
    elif saturday == "Wind rain":
        saturdayicon = "<span class='fs1 climacon wind cloud' aria-hidden='true'></span>"
    elif saturday == "Drizzle":
        saturdayicon = "<span class='fs1 climacon drizzle' aria-hidden='true'></span>"
    elif saturday == "Windy":
        saturdayicon = "<span class='fs1 climacon wind' aria-hidden='true'></span>"
    elif saturday == "Thunder":
        saturdayicon = "<span class='fs1 climacon lightning' aria-hidden='true'></span>"
    else:
        saturdayicon = ""

    if sunday == "Partly cloudy":
        sundayicon = "<span class='fs1 climacon cloud sun' aria-hidden='true'></span>"
    elif sunday == "Few showers":
        sundayicon = "<span class='fs1 climacon showers sun' aria-hidden='true'></span>"
    elif sunday == "Showers":
        sundayicon = "<span class='fs1 climacon showers' aria-hidden='true'></span>"
    elif sunday == "Rain":
        sundayicon = "<span class='fs1 climacon rain' aria-hidden='true'></span>"
    elif sunday == "Fine":
        sundayicon = "<span class='fs1 climacon sun' aria-hidden='true'></span>"
    elif sunday == "Cloudy":
        sundayicon = "<span class='fs1 climacon cloud' aria-hidden='true'></span>"
    elif sunday == "Wind rain":
        sundayicon = "<span class='fs1 climacon wind cloud' aria-hidden='true'></span>"
    elif sunday == "Drizzle":
        sundayicon = "<span class='fs1 climacon drizzle' aria-hidden='true'></span>"
    elif sunday == "Windy":
        sundayicon = "<span class='fs1 climacon wind' aria-hidden='true'></span>"
    elif sunday == "Thunder":
        sundayicon = "<span class='fs1 climacon lightning' aria-hidden='true'></span>"
    else:
        sundayicon = ""

    pressuredirection = r.get("pressureDirection")
    if pressuredirection in ("up", "upslowly", "upslowly-goodcoming"):
        pressuredirectionicon = "<ion-icon name='arrow-up-outline'></ion-icon>"
    elif pressuredirection in ("down", "downslowly", "downslowly-nogoodcoming"):
        pressuredirectionicon = "<ion-icon name='arrow-down-outline'></ion-icon>"
    elif pressuredirection == "stable":
        pressuredirectionicon = "<ion-icon name='arrow-forward-outline'></ion-icon>"
    else:
        pressuredirectionicon = ""

    html = todayforecast + "<br>"
    html += "Max: " + todaymax + "&deg;  Min: " + todaymin + "&deg;<br><br>"
    html += "<div class='counter-title'>The Forecast for Tomorrow</div>"
    html +=  tomorrowforecast + "<br> Max: " +  tomorrowmax + "&deg;  Min: " + tomorrowmin + "&deg;<br>"


    return render_template('weather.html', barometer = barometer, pressuredirectionicon = pressuredirectionicon, html = html,
                            saturdayicon = saturdayicon, sundayicon = sundayicon)
    

