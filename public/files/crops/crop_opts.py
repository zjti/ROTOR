import json


crop_opts = json.loads("""
{
    "ANBAU":{
        "lang_key":"Anbau",
        "type": "tab",
        "parent":"root"
    },
    "ERTRAG":{
        "lang_key": "Ertrag",
        "type":"tab",
        "parent":"root"
    },
    "DUNG":{
        "lang_key": "Dünger",
        "type":"tab",
        "parent":"root"
    }, 
    "CATH_CROP":{
        "type": "bool",
        "lang_key": "Zwischenfrucht_select",
        "parent": "ANBAU"
    },
    "BYPRODUCT_HARVEST":{
        "type": "bool",
        "lang_key": "Nebenprodukternte",
        "parent": "ANBAU"
    },
    "MP_YIELD":{
        "lang_key": "YIELD_TOTAL",
        "type": "float",
        "min" : 0,
        "max" : 100,
        "parent" : "ERTRAG"
    },
     "MP_YIELD_FROM_FERT":{
        "lang_key": "YIELD_FROM_FERT",
        "type": "float",
        "min" : 0,
        "max" : 100,
        "parent" : "ERTRAG"
    },
    "BP_YIELD":{
        "lang_key": "BYPRODUCT_TOTAL",
        "type": "float",
        "min" : 0,
        "max" : 100,
        "parent" : "ERTRAG"
    },
    "FERT":{
        "type" : "dung_select",
        "parent" : "DUNG"
    },
    "SCHNITT_NUTZ":{
        "type" : "schnitt_select",
        "parent" : "SCHNITT"
    }
    
}

""")

# def get_cropopt_ui(opts):
#     R = {}
#     E = {}
#     for opt in opts:
#         if opt not in crop_opts:
#             continue
#         copt = crop_opts[opt]
    
#         if copt['parent'] not in R:
#             R[copt['parent']] = copt
            
    