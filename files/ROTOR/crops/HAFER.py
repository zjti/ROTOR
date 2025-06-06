
from ROTOR.cerial import SummerCerial
from ROTOR.crops.data import cropdata
from ROTOR.utils import config


class HAFER(SummerCerial): 

    price_yield_eur_per_dt_fm = 19.00
    seed_cost_eur_per_kg = 0.8
    seed_kg_per_ha = 120

    
    def __init__(self,*args,**kwargs):
        super().__init__(crop_data = cropdata.HAFER, *args, **kwargs)

        
        
         
    def calc_yield_dt_fm_per_ha(self):
        EF= 2
        AZ = config.SOIL['ACKERZAHL']['default']
        #'y = -0.0081x2 + 1.367x - 8.8929
        #'y = -0.0072x2 + 1.2292x - 10.5
        #'y = -0,0062x2 + 1,0902x - 12,10
        if EF == 3:
            E = -0.0081 *AZ**2 + 1.367 *AZ - 8.8929
        elif EF == 2:
            E =  -0.0072 * AZ**2 + 1.2292 * AZ- 10.5
        elif EF == 1:
            E = -0.0062 * AZ**2 + 1.0902 * AZ - 12,10

        E += self.calc_yield_from_fertilizer_dt_fm_per_ha()
        return E

  