SOIL = {}
PHYTO_DELAY = {}
FFolge = {}
py_FFolge = {}
PHYTO_DELAY_TIME = {} 
DUNG_DATA = {}

import json
def jupyter_load_config():
    global FFolge

    with open('/drive/config_data/FFolge.json') as f:
        FFolge = json.load(f)