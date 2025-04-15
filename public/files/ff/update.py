import json
import config


from crops.utils import get_crop_dict

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

def updateFF(ffolge ):

    global old_ffolge_json,crop_dict
    
    if json.dumps(ffolge, sort_keys=True, indent=2) == old_ffolge_json:
        # print('nothing new')
        return None
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
                return None
            # print('diffs',diffs)
                     
        print('updating..')

    #update py_folge
    for k,val in ffolge.items():
        if val['crop'] not in crop_dict:
            continue

        if k not in config.FFolge:
            config.FFolge[k] = ffolge[k]
        config.FFolge[k].update(ffolge[k])
        
        if k in py_FFolge:
            if type(py_FFolge[k]) != crop_dict[val['crop']]:   
                py_FFolge[k] = crop_dict[val['crop']](k)    
        else:
            py_FFolge[k] = crop_dict[val['crop']](k)

   
    for k,val in py_FFolge.items():
        

        #update models
        models, always_update , always_remove = val.get_models()
        for modname,modval in models.items():
            if modname not in ffolge[k]:
                ffolge[k][modname] = modval
            if modname in always_update:
                ffolge[k][modname] = modval
        for modname in always_remove:
            if modname in ffolge[k]:
                del ffolge[k][modname]

        #update vis
        ffolge[k]['vis'] = val.get_vis()
        if 'dung_tab' in ffolge[k]['vis']:
            if 'dung_menge' not in ffolge[k]:
                ffolge[k]['dung_menge'] = {}
        if 'zw' in models:
            ffolge[k]['vis']['zw_opt'] = True
            ffolge[k]['vis']['anbau_tab'] = True
        if 'stroh' in models:
            ffolge[k]['vis']['stroh_opt'] = True
            ffolge[k]['vis']['anbau_tab'] = True
        if 'us' in models:
            ffolge[k]['vis']['us_opt'] = True
            ffolge[k]['vis']['anbau_tab'] = True


    
    config.FFolge = ffolge
    config.py_FFolge = py_FFolge
    old_ffolge_json = json.dumps(ffolge, sort_keys=True, indent=2) 
    
    return ffolge
    