import json
import config


from crops.utils import get_crop_dict
from crops.crop import FFolge

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
        if old_key in config.py_FFolge:
            del config.py_FFolge[old_key]
    
    return ffolge


old_ffolge_json = None

py_FFolge = {}
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
    global old_ffolge_json
    print('1')
 
    if not has_changes(ffolge):
        return None
    
    pyFolge = FFolge( len(ffolge) )
    
    for k,val in ffolge.items():
        if 'crop' not in val:
            pyFolge.add_crop(None)
            continue

        if val['crop'] not in crop_dict:
            pyFolge.add_crop(None)
            continue

        pyFolge.add_crop( crop_dict[val['crop']]() )
        

    print(pyFolge.crops)
    
    ffolge = pyFolge.serialize()
    ffolge = json.dumps(ffolge)
    
    old_ffolge_json = ffolge
    return ffolge
    