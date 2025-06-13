
from ROTOR.utils import config
from ROTOR.crop import Crop
from ROTOR.crops.data import cropdata
from .legray import calcLG

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue,ClassWithModelValues
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         
from ROTOR.management.workstep import  HarvestStep, ByproductHarvestStep, DrillStep,SeedBedPreparationStep,YieldTransportStep

from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils.js.jsmodel import ModelFields as MF

from ROTOR.utils import datehelper

class CutSelect(  ClassWithModelValues ):

    def __init__(self, num_cuts=4, *args, **kwargs):
        super().__init__( *args, **kwargs,model_value_group_name='cut_select')

        self.cut_amount_fm = [11,12,13,14,15]
        self.num_cuts = num_cuts
        UserEditableModelValue('num_cuts',self.get_num_cuts )
        UserEditableModelValue(f'cut1',self.get_cut1, unit='FM dt/ha' )
        UserEditableModelValue(f'cut2',self.get_cut2, unit='FM dt/ha' )
        UserEditableModelValue(f'cut3',self.get_cut3, unit='FM dt/ha' )
        UserEditableModelValue(f'cut4',self.get_cut4, unit='FM dt/ha' )
        UserEditableModelValue(f'cut5',self.get_cut5, unit='FM dt/ha' )

        UserEditableModelValue(f'nutz1',self.get_nutz1, type='select', select_opts=['grünfutter','heu','silage','mulch']) 
        UserEditableModelValue(f'nutz2',self.get_nutz2, type='select', select_opts=['grünfutter','heu','silage','mulch']) 
        UserEditableModelValue(f'nutz3',self.get_nutz3, type='select', select_opts=['grünfutter','heu','silage','mulch']) 
        UserEditableModelValue(f'nutz4',self.get_nutz4, type='select', select_opts=['grünfutter','heu','silage','mulch']) 
        UserEditableModelValue(f'nutz5',self.get_nutz5, type='select', select_opts=['grünfutter','heu','silage','mulch']) 
        
    def get_num_cuts(self):
        return self.num_cuts
    
    def get_cut(self,n):
        if self.get_nutz1()=='mulch':
            return 0
        if self.get_nutz1()=='heu':
            return self.cut_amount_fm[n]  * 0.3 * (0.65)
        if self.get_nutz1()=='silage':
            return self.cut_amount_fm[n]  * 0.71 * (0.85)
        return self.cut_amount_fm[n]
        
    
    def get_cut1(self):
        return self.get_cut(0)
        
    def get_cut2(self):
        return self.get_cut(1)
    
    def get_cut3(self):
        return self.get_cut(2)
    
    def get_cut4(self):
        return self.get_cut(3)
    
    def get_cut5(self):
        return self.get_cut(4)

    def get_nutz1(self):
        return 'grünfutter'
    def get_nutz2(self):
        return 'grünfutter'
    def get_nutz3(self):
        return 'grünfutter'
    def get_nutz4(self):
        return 'grünfutter'
    def get_nutz5(self):
        return 'grünfutter'
    

class LEG_GRAS(Crop):
    
    price_yield_eur_per_dt_fm = 5.00
    seed_cost_eur_per_kg = 0.1
    seed_kg_per_ha = 200

    
    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.LEG_GRAS,*args,**kwargs)
        UserEditableModelValue('schnitt_menge', self.get_schnitt_menge, tab = VF.schnitt_tab, visible=False)
        UserEditableModelValue('seed_kg_per_ha',self.get_seed_kg_per_ha,tab = VF.anbau_tab )

        self.cut_sel = CutSelect(num_cuts=3, model_value_ref = self)
        # ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)


    def get_schnitt_menge(self):
        cuts = calcLG({})
        schnitte = {}

        self.cut_sel.num_cuts = len(cuts)
        
        for i in range(5):
            self.cut_sel.cut_amount_fm[i] = 0
            getattr(self.cut_sel, f'get_cut{i+1}').visible = False
            getattr(self.cut_sel, f'get_nutz{i+1}').visible = False
        
        
        for i in range(self.cut_sel.get_num_cuts()):
            getattr(self.cut_sel, f'get_cut{i+1}').visible = True
            getattr(self.cut_sel, f'get_nutz{i+1}').visible = True
            
        for i,(n,date,menge) in enumerate(cuts):
            schnitte[str(n)] = {'yield': int(100*(menge*10))/100, 'nutz':'grünfutter', 'date':datehelper.day_index_to_half_month(date)}
            # if str(n) in old_cuts and 'nutz' in old_cuts[str(n)]:
    #         schnitte[str(n)]['nutz'] = old_cuts[str(n)]['nutz']
            self.cut_sel.cut_amount_fm[i] = int(100*(menge*10))/100
            

    
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