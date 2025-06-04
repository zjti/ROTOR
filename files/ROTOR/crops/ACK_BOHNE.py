from ROTOR.crop import Crop
from ROTOR.crops.data import cropdata

class ACK_BOHNE(Crop):
    
    def __init__(self):
        print('ackca2')
        crop_data = cropdata.ACK_BOHNE
        
        super().__init__(crop_data)

    def calc_yield_dt_fm_per_ha(self):
        AZ = config.SOIL['ACKERZAHL']['default']
        E = (-0.0111 * AZ ** 2 + 1.867 * AZ - 30.3)
        return E
    
    
    

    def get_crop_opts(self):
        return ["ZW_VOR","ZW_NACH","US_VOR"]