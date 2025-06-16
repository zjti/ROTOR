from ROTOR.utils.find_crops import get_crop_dict
from ROTOR.utils import config
import json

crop_dict = get_crop_dict()
all_crops = list(crop_dict.keys())

def get_avail_crops_for_jahr(ffolge, jahr ):
    
    ff_comp = ffolge[str(jahr)]
    ff_length = len(ffolge)
    
    # print(ff_comp['restr_select_phyto'] ,ff_comp['restr_select_time'])
    FORBIDEN_CROPS = set()
    for k,val in ffolge.items():
        if k == 'FF_META':
            continue
        kint = int(k)
        if kint==jahr:
            continue
        kdiff = min(abs(kint - jahr), ff_length - abs( kint-jahr) )
        if 'restr_select_phyto' in ff_comp and ff_comp['restr_select_phyto']:
            if 'crop' in val and val['crop'] in config.PHYTO_DELAY:
                #'DINKEL': {'delay': 2}, 'SM_WEIZEN': {'delay': 2}, 'WN_WEIZEN': {'delay': 2}, 'ACK_BOHNE': {'delay': 0}}
                for otherCrop, data in config.PHYTO_DELAY[val['crop']].items():
                    # print(otherCrop, data)
                    if data['delay'] >= kdiff:
                        # print(k,kdiff, otherCrop,data['delay'])
                        FORBIDEN_CROPS.add(otherCrop)
        if 'restr_select_time' in ff_comp and ff_comp['restr_select_time']:
            if 'crop' in val and val['crop'] in config.PHYTO_DELAY_TIME:
                #'DINKEL': {'delay': 2}, 'SM_WEIZEN': {'delay': 2}, 'WN_WEIZEN': {'delay': 2}, 'ACK_BOHNE': {'delay': 0}}
                for otherCrop, data in config.PHYTO_DELAY_TIME[val['crop']].items():
                    if data['delay'] >= kdiff:
                        # print(k,kdiff, otherCrop,data['delay'])
                        FORBIDEN_CROPS.add(otherCrop)

    # selected crop should not be removed. 
    if 'crop' in ff_comp and ff_comp['crop'] in FORBIDEN_CROPS:
        FORBIDEN_CROPS.remove(ff_comp['crop'])
        
    # print('RESTR jahr.: ',jahr,FORBIDEN_CROPS)
    return json.dumps([crop for crop in all_crops if crop not in FORBIDEN_CROPS ] )
        
       
    
    
    
    