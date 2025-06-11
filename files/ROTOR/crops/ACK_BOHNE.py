from ROTOR.crop import Crop
from ROTOR.crops.data import cropdata
from ROTOR.utils import config

class ACK_BOHNE(Crop):
    
    
    price_yield_eur_per_dt_fm = 59.00
    seed_cost_eur_per_kg = 1.5
    seed_kg_per_ha = 120
    
    def __init__(self,*args,**kwargs):
        super().__init__(crop_data = cropdata.ACK_BOHNE, *args, **kwargs)


    def calc_yield_dt_fm_per_ha(self):
        AZ = config.SOIL['ACKERZAHL']['default']
        E = (-0.0111 * AZ ** 2 + 1.867 * AZ - 30.3)
        return E
    
    
    

    def get_crop_opts(self):
        return ["ZW_VOR","ZW_NACH","US_VOR"]