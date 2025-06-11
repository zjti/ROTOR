from ROTOR.cerial import WinterCerial
from ROTOR.crops.data import cropdata
from ROTOR.utils import config

class TRITICALE(WinterCerial):


    price_yield_eur_per_dt_fm = 30.00
    seed_cost_eur_per_kg = 0.7
    seed_kg_per_ha = 200

    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.TRITICALE,*args,**kwargs)
        
        

    def calc_yield_dt_fm_per_ha(self,EF=2):
         
        AZ = config.SOIL['ACKERZAHL']['default']
        
        if EF == 3:
            E = -0.0074 * AZ ** 2 + 1.64 * AZ - 13.6
        elif EF == 2:
            E = -0.0067 * AZ ** 2 + 1.47 * AZ - 15
        elif EF == 1:
            E = -0.0059 * AZ ** 2 + 1.3 * AZ - 14.4
            
        E += self.calc_yield_from_fertilizer_dt_fm_per_ha()

        return E

    def get_vis(self):
        return {'ertrag_tab':True, 'dung_tab':True}
    
    def get_primary_product_nitrogen_kg_per_dt(self): 
        return self.get_primary_product_crude_protein_percentage() / 6.25
    
  
        
    def get_crop_opts(self):
        return ["STROH","ZW_VOR","ZW_NACH","US_VOR","US_NACH","DUNG","REDUCED","HAS_HERBST"]