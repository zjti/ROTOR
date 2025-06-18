
from ROTOR.utils import config
from ROTOR.crop import Crop
from ROTOR.crops.data import cropdata
from .legray import calcLG

from ROTOR.management.fertilizer import FertilizerApplications

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue,ClassWithModelValues
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         
from ROTOR.management.workstep import  HarvestStep, ByproductHarvestStep, DrillStep,SeedBedPreparationStep,YieldTransportStep

from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils.js.jsmodel import ModelFields as MF

from ROTOR.utils import datehelper
from ROTOR.economy.economy import CropEconomy
from ROTOR.management import workstep
from ROTOR.management.workstep import WorkStep, WorkStepList


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
        
    def get_nutz(self,n):
        return getattr(self, f"get_nutz{n+1}").__call__()
    
    def get_cut(self,n):
        
        if self.get_nutz(n)=='heu':
            return self.cut_amount_fm[n]  * 0.3 * (0.65)
        if self.get_nutz(n)=='silage':
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
    
    def all_nutz(self):
        nutzis = []
        for i in range(self.get_num_cuts()):
            nutzis += [ getattr(self, f'get_nutz{i+1}').__call__()  ]
        return nutzis
    
    def get_yield_silage_dt_fm_per_ha(self):
        M = 0
        for i in range(self.get_num_cuts()):
            if getattr(self, f'get_nutz{i+1}').__call__()  =='silage':
                M += getattr(self, f'get_cut{i+1}').__call__() 
        return M
    
    def get_yield_heu_dt_fm_per_ha(self):
        M = 0
        for i in range(self.get_num_cuts()):
            if getattr(self, f'get_nutz{i+1}').__call__()  =='heu':
                M += getattr(self, f'get_cut{i+1}').__call__() 
        return M
    
    def get_yield_grünfutter_dt_fm_per_ha(self):
        M = 0
        for i in range(self.get_num_cuts()):
            if getattr(self, f'get_nutz{i+1}').__call__()  =='grünfutter':
                M += getattr(self, f'get_cut{i+1}').__call__() 
        return M
    

class LGCropEconomy(CropEconomy):

    def __init__(self,  *args,**kwargs):
        super().__init__(*args,**kwargs)

    
        self.get_price_yield_eur_per_dt_fm.visible=False
        self.get_yield_leistung_eur_per_ha.visible=False
        
        print(self.crop.cut_sel.all_nutz(),'11')
        if 'grünfutter' in self.crop.cut_sel.all_nutz():
            print(self.crop.cut_sel.all_nutz(),'22')
            UserEditableModelValue('price_yield_grünfutter_eur_per_dt_fm', self.get_price_yield_grünfutter_eur_per_dt_fm, tab=VF.eco_tab , unit = '€/dt')
            ModelValue('yield_grünfutter_leistung_eur_per_ha', self.get_yield_grünfutter_leistung_eur_per_ha, tab=VF.eco_tab , unit = '€/ha')
        if 'heu' in self.crop.cut_sel.all_nutz():
            print(self.crop.cut_sel.all_nutz(),'22')
            UserEditableModelValue('price_yield_heu_eur_per_dt_fm', self.get_price_yield_heu_eur_per_dt_fm, tab=VF.eco_tab , unit = '€/dt')
            ModelValue('yield_heu_leistung_eur_per_ha', self.get_yield_heu_leistung_eur_per_ha, tab=VF.eco_tab , unit = '€/ha')
        if 'silage' in self.crop.cut_sel.all_nutz():
            print(self.crop.cut_sel.all_nutz(),'22')
            UserEditableModelValue('price_yield_silage_eur_per_dt_fm', self.get_price_yield_silage_eur_per_dt_fm, tab=VF.eco_tab , unit = '€/dt')
            ModelValue('yield_silage_leistung_eur_per_ha', self.get_yield_silage_leistung_eur_per_ha, tab=VF.eco_tab , unit = '€/ha')
            
        # worksteplist = WorkStepList(model_value_ref=self)
        # self.worksteplist = worksteplist

        
        # worksteplist.add(workstep.DrillStep(crop=self.crop))

    
    def get_price_yield_grünfutter_eur_per_dt_fm(self):
        return 5
    
    def get_price_yield_heu_eur_per_dt_fm(self):
        return 15

    def get_price_yield_silage_eur_per_dt_fm(self):
        return 7
    
    def get_yield_silage_leistung_eur_per_ha(self):
        return self.get_price_yield_silage_eur_per_dt_fm() * self.crop.cut_sel.get_yield_silage_dt_fm_per_ha() 
    
    def get_yield_heu_leistung_eur_per_ha(self):
        return self.get_price_yield_heu_eur_per_dt_fm() * self.crop.cut_sel.get_yield_heu_dt_fm_per_ha() 
    
    def get_yield_grünfutter_leistung_eur_per_ha(self):
        return self.get_price_yield_grünfutter_eur_per_dt_fm() * self.crop.cut_sel.get_yield_grünfutter_dt_fm_per_ha() 
    
    
    # pass
        
class LEG_GRAS(Crop):
    
    price_yield_eur_per_dt_fm = 5.00
    seed_cost_eur_per_kg = 8.5
    seed_kg_per_ha = 20

    
    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.LEG_GRAS,*args,**kwargs)
        self.fertilizer_applications = FertilizerApplications( model_value_ref = self )

        UserEditableModelValue('schnitt_menge', self.get_schnitt_menge, tab = VF.schnitt_tab, visible=False)
        UserEditableModelValue('seed_kg_per_ha',self.get_seed_kg_per_ha,tab = VF.anbau_tab )
        
        ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)
        
        UserEditableModelValue('reduced_soil_management',
                               self.get_reduced_soil_management,
                               type='bool', tab = VF.anbau_tab )
        
        UserEditableModelValue('get_cultivation',self.get_cultivation ,
                               tab=VF.anbau_tab,visible=True, type='select', 
                               select_opts=self.get_cultivation_options )

        UserEditableModelValue('get_leguminosen_percentage',self.get_leguminosen_percentage ,tab=VF.anbau_tab,visible=True)
        ModelValue('yield_dt_fm_per_ha',
                               self.calc_yield_dt_fm_per_ha,
                                )

        self.cut_sel = CutSelect(num_cuts=3, model_value_ref = self)
        
    def get_leguminosen_percentage(self):
        return 39
    
    def get_cultivation(self):
        if self.pre_crop:
            if self.pre_crop.crop_data.crop_code == 'LEG_GRAS':
                return 'VORJAHR'
        return 'HERBST'
    
    def get_seed_kg_per_ha(self):
        if self.pre_crop:
            if self.pre_crop.crop_data.crop_code == 'LEG_GRAS':
                return 0 
        return self.seed_kg_per_ha
    
    def get_cultivation_options(self):
        opts = ['FRÜHJAHR','HERBST']
        if self.pre_crop:
            if self.pre_crop.supports_undersowing():
                opts += ['UNTER_SAAT']
            
            if self.pre_crop.crop_data.crop_code == 'LEG_GRAS':
                opts = ['VORJAHR']
        return opts

    def autumn_fertelizer_application(self):
        return True
        # return not self.get_spring_sowing()
    
    def get_spring_sowing(self):
        return self.get_cultivation() == "FRÜHJAHR"

    def get_schnitt_menge(self):
        cuts = calcLG({},spring_seeding= self.get_spring_sowing())
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
        self.cut_sel = CutSelect(num_cuts=3, model_value_ref = self)

        super().post_init()

        self.economy = LGCropEconomy(crop=self, model_value_ref = self)
        

    
 
    def calc_yield_dt_fm_per_ha(self):
        
        E = 0
        E+= self.cut_sel.get_yield_silage_dt_fm_per_ha()
        
        E+= self.cut_sel.get_yield_heu_dt_fm_per_ha()
        
        E+= self.cut_sel.get_yield_grünfutter_dt_fm_per_ha()
        return E
    
    def get_worksteps(self):
        worksteps = []
        
        fertilizer_automn_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=True, for_spring=False)
        fertilizer_spring_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=False, for_spring=True)
    
        if fertilizer_automn_t_per_ha > 0:
            worksteps.append( FertilizerStep(date='OKT1' ,crop=self) ) 
        if fertilizer_spring_t_per_ha > 0:
            worksteps.append( FertilizerStep(date='MRZ2' ,crop=self) )

        
        if (self.pre_crop is None) or (self.pre_crop.crop_data.crop_code != 'LEG_GRAS') :
            if  self.get_cultivation() != "UNTER_SAAT":
                if self.get_reduced_soil_management():
                    self.reduced_primary_tilage_step.date = self.primary_tilage_step.date
                    worksteps.append( workstep.ReducedPrimaryTilageStep(date='SEP1',crop=self))
                else:
                    worksteps.append( workstep.PrimaryTilageStep(date='SEP1',crop=self))

                worksteps.append( workstep.SeedBedPreparationStep(date='SEP2',crop=self))
                worksteps.append( workstep.DrillStep(date='SEP2',crop=self))
            
        
        # try:
        schnitte = self.get_schnitt_menge()
        print(schnitte)
        for i,S in enumerate(schnitte.values()):          
            # worksteps.append( workstep.HarvestStep(date=S['date'],crop=self))
            if self.cut_sel.get_nutz(i) == 'grünfutter':
                worksteps.append( workstep.WorkStep(name=f"Mähen und bergen (Schnitt{i})",
                                                    machine_cost_eur_per_ha=30,
                                                    man_hours_h_per_ha=3,
                                                    diesel_l_per_ha=16, date=S['date'],crop=self))
            if self.cut_sel.get_nutz(i) == 'heu':
                worksteps.append( workstep.WorkStep(name=f"Mähen, schwaden, wenden und bergen (Schnitt{i})",
                                                    machine_cost_eur_per_ha=40,
                                                    man_hours_h_per_ha=5,
                                                    diesel_l_per_ha=23, date=S['date'],crop=self))
            
            if self.cut_sel.get_nutz(i) == 'silage':
                worksteps.append( workstep.WorkStep(name=f"Mähen, schwaden, wenden, bergen und silieren (Schnitt{i})",
                                                    machine_cost_eur_per_ha=35,
                                                    man_hours_h_per_ha=4,
                                                    diesel_l_per_ha=19, date=S['date'],crop=self))
            if self.cut_sel.get_nutz(i) == 'mulch':
                worksteps.append( workstep.WorkStep(name=f"Mähen (Schnitt{i})",
                                                    machine_cost_eur_per_ha=5,
                                                    man_hours_h_per_ha=0.7,
                                                    diesel_l_per_ha=3, date=S['date'],crop=self))
        # except:
        #     pass
         
        return worksteps
        
    
    def get_vis(self):
        return {'schnitt_tab':True,'anbau_tab':True,'leg_ansaat':True}
    
    def get_P_balance(self):
        P = 0
        if hasattr(self,'fertilizer_applications'):
            n,p,k = self.fertilizer_applications.get_NPK_from_fert_kg_per_ha()
            P += p
            
        
        P -= self.calc_yield_dt_fm_per_ha() * 0.19
            
        return P
    
    def get_N_removal(self):
        N = 0
        N += 1.1 * self.calc_yield_dt_fm_per_ha() 
        
        return N
    
    def get_N_from_fert(self):
        N=0
        if hasattr(self,'fertilizer_applications'):
            n,p,k = self.fertilizer_applications.get_NPK_from_fert_kg_per_ha()
            N+=n
        return N
    
    def get_K_balance(self):
        K = 0
        if hasattr(self,'fertilizer_applications'):
            n,p,k = self.fertilizer_applications.get_NPK_from_fert_kg_per_ha()
            K += k
            
        
        K -= self.calc_yield_dt_fm_per_ha() * 0.1
            
        return K
    
    
    
    def calc_N_total_fixation_kg_per_ha(self):
        F = 0
        
        F += 5 * self.calc_yield_dt_fm_per_ha() * self.get_leguminosen_percentage()/100
        
        
        return F
    
    def calc_N_leaching_kg_per_ha(self):
        return self.calc_yield_dt_fm_per_ha() * 0.02
