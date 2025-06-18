SOIL = {}
PHYTO_DELAY = {}
FFolge = {}
py_FFolge = {}
PHYTO_DELAY_TIME = {} 
DUNG_DATA = {}
PARAMS_USER ={}

import json
def jupyter_load_config():
    global FFolge, SOIL, DUNG_DATA,PARAMS_USER

    with open('/drive/config_data/FFolge.json') as f:
        FFolge = json.load(f)

    
    with open('/drive/config_data/SOIL.json') as f:
        SOIL = json.load(f)

    with open('/drive/config_data/DUNG_DATA.json') as f:
        DUNG_DATA = json.load(f)


    with open('/drive/config_data/PARAMS_USER.json') as f:
        PARAMS_USER = json.load(f)