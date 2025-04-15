from typing import Optional, Dict, Type
from .. import cropdata 
from .. import crop
import config

class ACK_BOHNE(crop.Leguminosen):
    
    def __init__(self,jahr_key):
        print('ackca2')
        crop_data = cropdata.ACK_BOHNE
        
        super().__init__(crop_data, jahr_key)

    def calc_yield_dt_fm_per_ha(self):
        AZ = config.SOIL['ACKERZAHL']['default']
        E = (-0.0111 * AZ ** 2 + 1.867 * AZ - 30.3)
        return E
    
    
    

    def get_crop_opts(self):
        return ["ZW_VOR","ZW_NACH","US_VOR"]