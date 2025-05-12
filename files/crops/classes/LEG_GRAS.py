from typing import Optional, Dict, Type
from .. import cropdata 
from .. import crop
import config
from .legray import calcLG

class LEG_GRAS(crop.Leguminosen):
    
    def __init__(self):
        crop_data = cropdata.LEG_GRAS
        
        super().__init__(crop_data)

    def calc_yield_dt_fm_per_ha(self):
        """ 
        returns dict  
        uses legray
        """
        spring_seeding = True
        # ffcomp = config.FFolge[self.jahr_key]
        # if 'leg_ansaat' in config.FFolge[self.jahr_key]:
            # spring_seeding = config.FFolge[self.jahr_key]['leg_ansaat'] == 'SPRING'

        # if 'schnitt_menge' in ffcomp:
        #     return calcLG( ffcomp['schnitt_menge'], spring_seeding=spring_seeding)
        # else:
            # return calcLG( {}, spring_seeding=spring_seeding)
        return calcLG( {}, spring_seeding=spring_seeding)
    
    def calc_byproduct_yield_dt(self):
        return 1.2
    
    def get_primary_product_nitrogen_kg_per_dt(self):
        return 1
    
    def get_N_uptake(self):
        return 10
    
    def get_vis(self):
        return {'schnitt_tab':True,'anbau_tab':True,'leg_ansaat':True}
    
    def get_models(self):
            
        ffcomp = config.FFolge[self.jahr_key]
        

        always_remove = []
        always_update  = ['schnitt_menge' ]
 
        roundoff = lambda x:  float(int(x *100 ) / 100) if x != 0 else 0
        # 'schnitt_menge': {'1': {'yield': 30, 'nutz': 'grünfutter'}, '2': {'y....
        yield_dt = self.calc_yield_dt_fm_per_ha()
        models = {'has_herbst_gabe':True, 'dung_menge':{} ,'schnitt_menge': yield_dt}

        # :items="FF[jahr].leg_ansaat_opts"
        # v-model="FF[jahr].leg_ansaat"
        
        models['leg_ansaat'] = 'SPRING'
        models['leg_ansaat_opts'] = ['SPRING','AUTUMN']
        
        pre_crop_key = int(self.jahr_key) - 1
        if pre_crop_key == 0:
            pre_crop_key = len(config.FFolge)
        pre_crop_key = str(pre_crop_key)
        print('prekey', pre_crop_key, self.jahr_key)
        if config.FFolge[pre_crop_key]['crop'] == 'LEG_GRAS':
            models['leg_ansaat'] = 'PREV_YEAR'
            models['leg_ansaat_opts'] = ['PREV_YEAR']

        # is undersawing an option ?
        us_opt = True
        
        if 'leg_ansaat' in ffcomp and ffcomp['leg_ansaat'] != 'AUTUMN':
            us_opt = False
        if 'leg_ansaat' not in ffcomp and models['leg_ansaat'] != 'AUTUMN':
            us_opt = False
            
        if pre_crop_key in config.py_FFolge:
            if 'US_NACH' not in config.py_FFolge[pre_crop_key].get_crop_opts():
                us_opt = False
        
        
        if us_opt:
            models['us'] = False
        else:
            always_remove+=['us'] 
             
 
        return models , always_update, always_remove
               
        

    def get_crop_opts(self):
        return ["DUNG"]