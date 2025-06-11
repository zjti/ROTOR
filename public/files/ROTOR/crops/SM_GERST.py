
from ROTOR.cerial import SummerCerial
from ROTOR.crops.data import cropdata
from ROTOR.utils import config


class SM_GERST(SummerCerial): 

    price_yield_eur_per_dt_fm = 33.00
    seed_cost_eur_per_kg = 0.8
    seed_kg_per_ha = 120

    
    def __init__(self,*args,**kwargs):
        super().__init__(crop_data = cropdata.SM_GERST, *args, **kwargs)

        
        
         
    def calc_yield_dt_fm_per_ha(self):
        EF= 2
        AZ = config.SOIL['ACKERZAHL']['default']
        if EF == 3:
            E = -0.0054 * AZ ** 2 + 1.28 * AZ - 13.7
        elif EF == 2:
            E = -0.0048 * AZ ** 2 + 1.15 * AZ - 13.7
        elif EF == 1:
            E = -0.0045 * AZ ** 2 + 1.07 * AZ - 14.2

     
        
        E += self.calc_yield_from_fertilizer_dt_fm_per_ha()
        return E

  