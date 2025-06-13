import json
from ROTOR.utils import config 
from ROTOR.utils import weather

from pyodide.ffi import to_js
from ROTOR.ff import update
from ROTOR.ff import restrictions

def JSupdateWeather(lat_lon_json):
    print('aaa')
    print('Upda te weather', lat_lon_json)
    lat_lon = json.loads(lat_lon_json)
    try:
        weather.load_from_lat_lon(lat_lon)
        print('gno' ,)
    except:
        pass
    # weather.load_from_lat_lon(lat_lon)

def JSdownload_eco_report():
    return config.pyFolge.ff_economy.write_report()

def JSupdateFF(f):
    return update.updateFF(f.to_py())

def JSupdateFFlength(f,jahre):
    return json.dumps(update.updateFFlength(f.to_py(),jahre))

def JSget_avail_crops_for_jahr(ffolge, jahr):
    x = restrictions.get_avail_crops_for_jahr(ffolge.to_py(), jahr)
    return x

def JSget_eval_data():
    return json.dumps(config.pyFolge.get_eval_data())
    # return json.dumps( config.... .get_eval_data())
