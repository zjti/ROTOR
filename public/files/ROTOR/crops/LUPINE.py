from ROTOR.crop import Crop
from ROTOR.grainlegum import SummerGrainLegum
from ROTOR.crops.data import cropdata
from ROTOR.utils import config
from ROTOR.utils.js.jsmodel import VisFields as VF

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         



class LUPINE(SummerGrainLegum):

    price_yield_eur_per_dt_fm = 65.00
    seed_cost_eur_per_kg = 1.30
    seed_kg_per_ha = 150
    
    def __init__(self, *args, **kwargs):
        super().__init__(cropdata.LUPINE, *args, **kwargs)
        
        self.hack_step = StriegelStep(name='Hacken', crop=self, date = 'MAI2',
                                    machine_cost_eur_per_ha=7.7,
                                    diesel_l_per_ha= 4,
                                    man_hours_h_per_ha= 0.55)


    
    def supports_undersowing(self):
        return False
    
    def get_crop_opts(self):
        return ["ZW_VOR","US_NACH","US_VOR"]
    
    def calc_yield_dt_fm_per_ha(self) -> float: 
        AZ = config.SOIL['ACKERZAHL']['default']
        
        E = -0.0072 * AZ ** 2 + 1.115 * AZ - 8.01 
        
        return E
            