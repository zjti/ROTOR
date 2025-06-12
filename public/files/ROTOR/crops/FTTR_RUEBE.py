from ROTOR.crop import Crop
from ROTOR.crops.data import cropdata
from ROTOR.utils import config
from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         
from ROTOR.management.workstep import  HarvestStep, ByproductHarvestStep, DrillStep,SeedBedPreparationStep,YieldTransportStep

from ROTOR.management.fertilizer import FertilizerApplications

from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils.js.jsmodel import ModelFields as MF
from ROTOR.management.workstep import WorkStep,WorkStepList,num_to_date,date_to_num
from ROTOR.covercrop import CoverCrop


class FTTR_RUEBE(Crop):

    price_yield_eur_per_dt_fm = 1.40
    seed_cost_eur_per_kg = 5.5
    seed_kg_per_ha = 20

    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.FTTR_RUEBE,*args,**kwargs)
         
        self.fertilizer_applications = FertilizerApplications( model_value_ref = self )
        UserEditableModelValue('seed_kg_per_ha',self.get_seed_kg_per_ha,tab = VF.anbau_tab )

        ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)
        UserEditableModelValue('reduced_soil_management',
                               self.get_reduced_soil_management,
                               type='bool', tab = VF.anbau_tab )
        
        UserEditableModelValue('yield_dt_fm_per_ha',
                               self.calc_yield_dt_fm_per_ha,
                               tab = VF.ertrag_tab, unit='FM dt/ha' )

        UserEditableModelValue('has_cover_crop',self.has_cover_crop ,tab=VF.anbau_tab,visible=True, type='bool')
    
    def post_init(self):
        """ should be called after __init__ and when ffolge is complete """
        
        if self.has_cover_crop():
            self.cover_crop = CoverCrop( ffelement = self , model_value_ref=self )
        
        super().post_init()
        

    def calc_yield_dt_fm_per_ha(self,EF=2):
        return 450

    def autumn_fertelizer_application(self):
        return True
    
    def get_seed_kg_per_ha(self) :
        return self.seed_kg_per_ha


    def supports_undersowing(self):
        return False

    def get_worksteps(self):
        worksteps = []
        
        fertilizer_automn_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=True, for_spring=False)
        fertilizer_spring_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=False, for_spring=True)
    
        if fertilizer_automn_t_per_ha > 0:
            worksteps.append( FertilizerStep(date='OKT1' ,crop=self) ) 
            
        
        if self.get_reduced_soil_management():
            worksteps.append( ReducedPrimaryTilageStep(date='OKT2',crop=self) )
        else:
            worksteps.append( PrimaryTilageStep(date='OKT2',crop=self))
        
        if self.has_cover_crop():
 
            
            if self.cover_crop.get_cultivation() == 'BLANK_SAAT':
                worksteps.append( WorkStep(name='Zwischenfruchtansaat (Blank)' ,date='SEP2' ,crop=self))
                
            if self.cover_crop.get_cultivation() == 'STOPPEL_SAAT':
                worksteps.append( WorkStep(name='Zwischenfruchtansaat (Stoppel)'  ,date='SEP2',crop=self))
                
            if self.cover_crop.get_cover_crop_harvest():
                worksteps.append( WorkStep(name='Zwischenfruchtabfuhr' ,date='MRZ2',crop=self))

     
            if self.get_reduced_soil_management():
                worksteps.append( ReducedPrimaryTilageStep('MRZ2',crop=self) )
            else:
                worksteps.append( PrimaryTilageStep('MRZ2',crop=self))

                

        if fertilizer_spring_t_per_ha > 0:
            worksteps.append( FertilizerStep(date='MRZ2' ,crop=self) )
            
            
        worksteps.append(SeedBedPreparationStep(date = 'MRZ2', diesel_l_per_ha=5.4,
                                                man_hours_h_per_ha=0.6,
                                                machine_cost_eur_per_ha= 15,crop=self))
        
        worksteps.append(WorkStep ('Einzelkornsaat',date='APR1',
                                   machine_cost_eur_per_ha=14, diesel_l_per_ha=4,
                                   man_hours_h_per_ha=0.6,crop=self))
        
        worksteps.append(WorkStep ('Hacken 1',date='APR2',
                                   machine_cost_eur_per_ha=9, diesel_l_per_ha=5.4,
                                   man_hours_h_per_ha=1.3,crop=self))
        
        worksteps.append(WorkStep ('Hacken 2',date='MAI1',
                                   machine_cost_eur_per_ha=9, diesel_l_per_ha=5.4,
                                   man_hours_h_per_ha=1.4,crop=self))
       
        worksteps.append(WorkStep ('Hacken 3',date='JUN1',
                                   machine_cost_eur_per_ha=9, diesel_l_per_ha=5.4,
                                   man_hours_h_per_ha=1.5,crop=self))
        
        worksteps.append(WorkStep ('Roden',date='SEP2',
                                   machine_cost_eur_per_ha=94, diesel_l_per_ha=40,
                                   man_hours_h_per_ha=4.3,crop=self))
        
       
        worksteps.append(YieldTransportStep(date='SEP2',crop=self, man_hours_h_per_ha=1.5))
        
       
       

        
        
        return worksteps