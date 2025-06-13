
from ROTOR.utils import config
from ROTOR.crop import Crop
from ROTOR.crops.data import cropdata
from .legray import calcLG

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         
from ROTOR.management.workstep import  HarvestStep, ByproductHarvestStep, DrillStep,SeedBedPreparationStep,YieldTransportStep

from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils.js.jsmodel import ModelFields as MF

class LEG_GRAS(Crop):
    
    price_yield_eur_per_dt_fm = 5.00
    seed_cost_eur_per_kg = 0.1
    seed_kg_per_ha = 200

    
    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.LEG_GRAS,*args,**kwargs)
        UserEditableModelValue('schnitt_menge', self.get_schnitt_menge, tab = VF.schnitt_tab, visible=False)
        UserEditableModelValue('seed_kg_per_ha',self.get_seed_kg_per_ha,tab = VF.anbau_tab )

        # ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)


    def get_schnitt_menge(self):
        cuts = calcLG({})
        schnitte = {}
        for n,date,menge in cuts:
            schnitte[str(n)] = {'yield': int(100*(menge*10))/100, 'nutz':'grünfutter'}
            # if str(n) in old_cuts and 'nutz' in old_cuts[str(n)]:
    #         schnitte[str(n)]['nutz'] = old_cuts[str(n)]['nutz']
    
        return schnitte
    
    def post_init(self):
        """ should be called after __init__ and when ffolge is complete """
        
         
        
        super().post_init()
    
 
    def calc_yield_dt_fm_per_ha(self):
        """ 
        returns dict  
        uses legray
        """
        # self.cuts = calcLG({})
        return 999
        spring_seeding = True
        # if 'leg_ansaat' in config.FFolge[self.jahr_key]:
        #     spring_seeding = config.FFolge[self.jahr_key]['leg_ansaat'] == 'SPRING'

        return calcLG( {}, spring_seeding=spring_seeding)
    
    def get_vis(self):
        return {'schnitt_tab':True,'anbau_tab':True,'leg_ansaat':True}
    
    # def get_models(self):
            
    #     ffcomp = config.FFolge[self.jahr_key]
        

    #     always_remove = []
    #     always_update  = ['schnitt_menge' ]
 
    #     roundoff = lambda x:  float(int(x *100 ) / 100) if x != 0 else 0
    #     # 'schnitt_menge': {'1': {'yield': 30, 'nutz': 'grünfutter'}, '2': {'y....
    #     yield_dt = self.calc_yield_dt_fm_per_ha()
    #     models = {'has_herbst_gabe':True, 'dung_menge':{} ,'schnitt_menge': yield_dt}

    #     # :items="FF[jahr].leg_ansaat_opts"
    #     # v-model="FF[jahr].leg_ansaat"
        
    #     models['leg_ansaat'] = 'SPRING'
    #     models['leg_ansaat_opts'] = ['SPRING','AUTUMN']
        
    #     pre_crop_key = int(self.jahr_key) - 1
    #     if pre_crop_key == 0:
    #         pre_crop_key = len(config.FFolge)
    #     pre_crop_key = str(pre_crop_key)
    #     print('prekey', pre_crop_key, self.jahr_key)
    #     if config.FFolge[pre_crop_key]['crop'] == 'LEG_GRAS':
    #         models['leg_ansaat'] = 'PREV_YEAR'
    #         models['leg_ansaat_opts'] = ['PREV_YEAR']

    #     # is undersawing an option ?
    #     us_opt = True
        
    #     if 'leg_ansaat' in ffcomp and ffcomp['leg_ansaat'] != 'AUTUMN':
    #         us_opt = False
    #     if 'leg_ansaat' not in ffcomp and models['leg_ansaat'] != 'AUTUMN':
    #         us_opt = False
            
    #     if pre_crop_key in config.py_FFolge:
    #         if 'US_NACH' not in config.py_FFolge[pre_crop_key].get_crop_opts():
    #             us_opt = False
        
        
    #     if us_opt:
    #         models['us'] = False
    #     else:
    #         always_remove+=['us'] 
             
 
    #     return models , always_update, always_remove
               
        

    # def get_crop_opts(self):
    #     return ["DUNG"]