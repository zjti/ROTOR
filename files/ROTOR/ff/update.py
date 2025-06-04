import json
from ROTOR.utils import config


from ROTOR.utils.find_crops import get_crop_dict
from ROTOR.ff.ffolge import FFolge

from ROTOR.utils.js.jsmodel import ModelFields as MF

def jahr_key(i):
    return str(i+1)

def updateFFlength(ffolge, NJahre):
    print(ffolge,NJahre)
    
    valid_keys = []
    for i in range(NJahre):
        k = jahr_key(i)
        valid_keys.append(k)
        if ( k not in ffolge):
            ffolge[k] = {'crop':'',
                        'vis':{},
                         'restr_select_phyto':False,
                         'restr_select_time':True,
                        }

    old_keys = [key for key in ffolge.keys() if key not in valid_keys ]
    for old_key in old_keys:
        del ffolge[old_key]
    
    return ffolge


old_ffolge_json = None
pyFolge = None
crop_dict = get_crop_dict()

def has_changes(ffolge):
    if json.dumps(ffolge, sort_keys=True, indent=2) == old_ffolge_json:
         return False
    else:
        if old_ffolge_json: 
            
            A=json.dumps(ffolge, sort_keys=True, indent=2).split()
            B=old_ffolge_json.split()
            diffs= 0
            for i,(a,b) in enumerate(zip(A,B)):
                if a!=b :
                    try:
                        if a[-1]==',':
                            a=a[:-1]
                            
                        if b[-1]==',':
                            b=b[:-1]
                        if float(a) == float(b):

                            diffs += 0
                        else:
                            diffs += 1
                            break
                    except:
                        diffs += 1
                        break
            if diffs == 0:
                return False
            # print('diffs',diffs)
                     
    return True

def updateFF(ffolge):
    """ 
        ffolge : nested dict
        returns : Json
    """
    global old_ffolge_json, pyFolge
 
    if not has_changes(ffolge):
        return old_ffolge_json
    
    pyFolge = FFolge( len(ffolge) )
    
    for val in ffolge.values():
        if MF.crop not in val:
            pyFolge.add_crop(None)
            continue

        if val[MF.crop] not in crop_dict:
            pyFolge.add_crop(None)
            continue
        
        new_crop = crop_dict[val[MF.crop]](model_values = val.get('MODELVALUES',None))
        # new_crop.deserialize( val )
        pyFolge.add_crop( new_crop )
        
    pyFolge.post_init()
    # print(pyFolge.crops)
    
    new_ffolge = pyFolge.serialize()
    
    for key in new_ffolge.keys():
        new_ffolge[key][MF.restr_select_phyto] = ffolge[key][MF.restr_select_phyto]
        new_ffolge[key][MF.restr_select_time] = ffolge[key][MF.restr_select_time]
        
    ffolge = json.dumps(new_ffolge)
    
    old_ffolge_json = ffolge
    
    #for debug only:
    config.FFolge = ffolge
    
    return ffolge
    
    
def get_eval_data():
    if pyFolge is not None:
        return pyFolge.get_eval_data()