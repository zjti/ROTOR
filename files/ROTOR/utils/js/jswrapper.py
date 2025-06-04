import json
import config 
from pyodide.ffi import to_js
from ROTOR.ff import update
from ROTOR.ff import restrictions

def JSupdateFF(f):
    return update.updateFF(f.to_py())


def JSupdateFFlength(f,jahre):
    return json.dumps(update.updateFFlength(f.to_py(),jahre))

def JSget_avail_crops_for_jahr(ffolge, jahr):
    x = restrictions.get_avail_crops_for_jahr(ffolge.to_py(), jahr)
    return x

def JSget_eval_data():
    return json.dumps([])
    # return json.dumps( config.... .get_eval_data())
