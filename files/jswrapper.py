import json
import config 
from pyodide.ffi import to_js
import ff.restrictions

from ff.calc_opts import calc_opts 
import ff

def updateFF(f):
    return ff.updateFF(f.to_py())


def updateFFlength(f,jahre):
    return json.dumps(ff.updateFFlength(f.to_py(),jahre))

def get_avail_crops_for_jahr(ffolge, jahr):
    x = ff.restrictions.get_avail_crops_for_jahr(ffolge.to_py(), jahr)
    return x

def get_eval_data():
    return json.dumps(ff.get_eval_data())
