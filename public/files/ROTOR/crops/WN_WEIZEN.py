from ROTOR.cerial import WinterCerial
from ROTOR.crops.data import cropdata
from ROTOR.utils import config

class WN_WEIZEN(WinterCerial):


    price_yield_eur_per_dt_fm = 49.00
    seed_cost_eur_per_kg = 0.7
    seed_kg_per_ha = 200

    
    
    """Winter wheat implementation"""
    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.WN_WEIZEN,*args,**kwargs)
        
        

    def calc_yield_dt_fm_per_ha(self,EF=2):
         
        AZ = config.SOIL['ACKERZAHL']['default']
        
        if EF == 3:
            E = -0.0053 * AZ**2 + 1.57 * AZ - 16.7
        elif EF == 2:
            E = -0.0047 * AZ**2 + 1.41 * AZ - 16.8
        elif EF == 1:
            E = -0.0042 * AZ**2 + 1.25 * AZ - 16.9
            
        E += self.calc_yield_from_fertilizer_dt_fm_per_ha()

        return E

    def get_vis(self):
        return {'ertrag_tab':True, 'dung_tab':True}
    
    def get_primary_product_nitrogen_kg_per_dt(self): 
        return self.get_primary_product_crude_protein_percentage() / 6.25
    
  
        
    def get_crop_opts(self):
        return ["STROH","ZW_VOR","ZW_NACH","US_VOR","US_NACH","DUNG","REDUCED","HAS_HERBST"]