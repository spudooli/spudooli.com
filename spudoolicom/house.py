from flask import render_template
from spudoolicom import app, db
import redis
import asyncio
from tapo import ApiClient

r = redis.from_url(app.config['REDIS_URL'], encoding="utf-8", decode_responses=True)


def _format_minutes(minutes):
    if minutes is None:
        return "-"
    minutes = int(minutes)
    if minutes == 0:
        return "0m"
    h, m = divmod(minutes, 60)
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"


_TAPO_CLIENT_METHODS = {
    'p100': 'p100',
    'p110': 'p110',
    'l530': 'l530',
}


def _format_watts(milliwatts):
    if milliwatts is None:
        return '-'
    return f"{milliwatts / 1000:.1f} W"


def _format_wh(wh):
    if wh is None:
        return '-'
    if wh >= 1000:
        return f"{wh / 1000:.2f} kWh"
    return f"{wh} Wh"


async def _fetch_tapo_device(client, device_cfg):
    device_type = device_cfg.get('type', 'p100')
    try:
        method = _TAPO_CLIENT_METHODS.get(device_type, 'p100')
        device = await getattr(client, method)(device_cfg['ip'])
        info = await device.get_device_info()
        usage = await device.get_device_usage()
        info_dict = info.to_dict()
        usage_dict = usage.to_dict()
        time_usage = usage_dict.get('time_usage', {})

        energy = None
        if device_type == 'p110':
            eu = await device.get_energy_usage()
            eu_dict = eu.to_dict()
            energy = {
                'current_power': _format_watts(eu_dict.get('current_power')),
                'today_energy':  _format_wh(eu_dict.get('today_energy')),
                'month_energy':  _format_wh(eu_dict.get('month_energy')),
            }

        return {
            'name': device_cfg.get('name') or info_dict.get('nickname', device_cfg['ip']),
            'ip': device_cfg['ip'],
            'type': device_type,
            'on': info_dict.get('device_on', False),
            'today': _format_minutes(time_usage.get('today')),
            'past7': _format_minutes(time_usage.get('past7')),
            'past30': _format_minutes(time_usage.get('past30')),
            'energy': energy,
            'error': None,
        }
    except Exception as e:
        return {
            'name': device_cfg.get('name') or device_cfg['ip'],
            'ip': device_cfg['ip'],
            'type': device_type,
            'on': None,
            'today': '-',
            'past7': '-',
            'past30': '-',
            'energy': None,
            'error': str(e),
        }


async def _fetch_all_tapo_devices():
    devices_cfg = app.config.get('TAPO_DEVICES', [])
    if not devices_cfg:
        return []
    client = ApiClient(app.config['TAPO_USERNAME'], app.config['TAPO_PASSWORD'])
    results = await asyncio.gather(*[_fetch_tapo_device(client, d) for d in devices_cfg])
    return list(results)


@app.route('/house')
def house():

    indoortemp = (r.get('indoorTemperature') or "?") + "&deg;"
    outdoortemp = (r.get('outdoorTemperature') or "?") + "&deg;"
    outdoorhumidity = (r.get('outsideHumidity') or "?") + "%"
    shedtemp = (r.get('gardenshedTemperature') or "?") + "&deg;"
    mancaveTemperature = (r.get('mancaveTemperature') or "?") + "&deg;"
    mancavehumidity = (r.get("mancaveHumidity") or "?") + "%"
    kitchenTemperature = (r.get("kitchenTemperature") or "?") + "&deg;"
    kitchenhumidity = (r.get("kitchenHumidity") or "?") + "%"
    centralheating = (r.get("heatTemperature") or "?") + "&deg;"
    centralheatinghumidity = (r.get("heatHumidity") or "?") + "%"
    fridgedoortoday = r.get("fridgeDoorCounter") or "0"
    barometer = r.get("indoorPressure") or "0hPa"
    barometer = barometer[0:-2]
    i3range = r.get("i3rangeremaining")
    i3battery = r.get("i3batteryremaining")

    waterTemp = r.get('spatemperature')
    if waterTemp == 0:
        waterTemp = "-"


    # Fridge door count
    cur = db.mysql.connection.cursor()
    cur.execute("SELECT sum(open_count) FROM fridge_door")
    fridgeDoorCount = cur.fetchone()
    unformattedFridgeDoorCount = fridgeDoorCount[0]
    fridgeDoorCount = int(unformattedFridgeDoorCount) + int(fridgedoortoday)
    fridgeDoorCount = "{:,}".format(fridgeDoorCount)
    cur.close()

    tapo_devices = asyncio.run(_fetch_all_tapo_devices())

    return render_template('house.html', waterTemp = waterTemp, barometer = barometer, fridgedoortoday = fridgedoortoday,
                          kitchenhumidity = kitchenhumidity, kitchenTemperature = kitchenTemperature, centralheatinghumidity = centralheatinghumidity,
                          shedtemp = shedtemp, centralheating = centralheating, mancaveTemperature = mancaveTemperature, fridgeDoorCount = fridgeDoorCount,
                          indoortemp = indoortemp, outdoortemp = outdoortemp, outdoorhumidity = outdoorhumidity, mancavehumidity = mancavehumidity, i3range = i3range, i3battery = i3battery,
                          tapo_devices = tapo_devices)
    
