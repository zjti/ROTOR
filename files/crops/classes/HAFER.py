from typing import Optional, Dict, Type
from .. import cropdata 
from .. import crop
import config


class HAFER(crop.SommerGetreide): 
    def __init__(self):
        crop_data = cropdata.HAFER
        
        super().__init__(crop_data)

    def calc_yield_dt_fm_per_ha(self,EF=2):
         
        AZ = config.SOIL['ACKERZAHL']['default']
        
        if EF == 3:
            E = -0.0053 * AZ**2 + 1.57 * AZ - 16.7
        elif EF == 2:
            E = -0.0047 * AZ**2 + 1.41 * AZ - 16.8
        elif EF == 1:
            E = -0.0042 * AZ**2 + 1.25 * AZ - 16.9
        return E

    def get_vis(self):
        return {'ertrag_tab':True, 'dung_tab':True}

 
        
    def get_crop_opts(self):
        return ["STROH","ZW_VOR","ZW_NACH","US_VOR","US_NACH","DUNG","REDUCED","HAS_HERBST"]