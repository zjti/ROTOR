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


class KRN_MAIS(Crop):

    price_yield_eur_per_dt_fm = 56.00
    seed_cost_eur_per_u = 140
    seed_u_per_ha = 2

    def __init__(self,*args,**kwargs):
        super().__init__(cropdata.KRN_MAIS,*args,**kwargs)
         
        self.fertilizer_applications = FertilizerApplications( model_value_ref = self )
        UserEditableModelValue('seed_u_per_ha',self.get_seed_u_per_ha,tab = VF.anbau_tab )

        ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)
        UserEditableModelValue('reduced_soil_management',
                               self.get_reduced_soil_management,
                               type='bool', tab = VF.anbau_tab )
        
        UserEditableModelValue('byproduct_harvest',
                               self.get_byproduct_harvest,
                               type='bool', tab = VF.anbau_tab )
        
        UserEditableModelValue('yield_dt_fm_per_ha',
                               self.calc_yield_dt_fm_per_ha,
                               tab = VF.ertrag_tab, unit='FM dt/ha' )

        UserEditableModelValue('calc_yield_from_fertilizer_dt_fm_per_ha',
                               self.calc_yield_from_fertilizer_dt_fm_per_ha,
                               tab = VF.ertrag_tab, unit='FM dt/ha' )

        UserEditableModelValue('byproduct_yield_dt_fm_per_ha',
                               self.calc_byproduct_yield_dt_fm_per_ha,
                               tab = VF.ertrag_tab,unit='FM dt/ha' )

        UserEditableModelValue('has_cover_crop',self.has_cover_crop ,tab=VF.anbau_tab,visible=True, type='bool')
    
    def post_init(self):
        """ should be called after __init__ and when ffolge is complete """
        
        if self.has_cover_crop():
            self.cover_crop = CoverCrop( ffelement = self , model_value_ref=self )
        
        super().post_init()
        
    def calc_yield_dt_fm_per_ha(self):
        EF= 2
        AZ = config.SOIL['ACKERZAHL']['default']
      
        if EF == 3:
            E = ((-0.024 * AZ ** 2 + 3.98 * AZ - 7) - 70 * 0.3) / 2.3 
        elif EF == 2:
            E = ((-0.02 * AZ ** 2 + 3.5 * AZ - 12) - 70 * 0.3) / 2.3
        elif EF == 1:
            E = ((-0.016 * AZ ** 2 + 3 * AZ - 17) - 70 * 0.3) / 2.3     

        E += self.calc_yield_from_fertilizer_dt_fm_per_ha()
        return E


    def autumn_fertelizer_application(self):
        return True
    
    def get_seed_u_per_ha(self) :
        return self.seed_u_per_ha


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
            
            
        worksteps.append(SeedBedPreparationStep(date = 'APR2', diesel_l_per_ha=13.4,
                                                man_hours_h_per_ha=1.2,
                                                machine_cost_eur_per_ha= 25,crop=self))
        
        worksteps.append(WorkStep ('Einzelkornsaat',date='APR2',
                                   machine_cost_eur_per_ha=14, diesel_l_per_ha=4,
                                   man_hours_h_per_ha=0.6,crop=self))
        
        worksteps.append(StriegelStep ('Strigeln',date='APR2',crop=self))
        
        worksteps.append(WorkStep ('Hacken 1',date='MAI1',
                                   machine_cost_eur_per_ha=9, diesel_l_per_ha=5.4,
                                   man_hours_h_per_ha=1.4,crop=self))
       
        worksteps.append(WorkStep ('Hacken 2',date='JUN1',
                                   machine_cost_eur_per_ha=9, diesel_l_per_ha=5.4,
                                   man_hours_h_per_ha=1.5,crop=self))
        
        if self.next_crop and  self.next_crop.has_cover_crop():
            if self.next_crop.cover_crop.get_cultivation() == 'UNTER_SAAT':
                unter_saat_date = 'APR1'
                worksteps.append( WorkStep(name='Zwischenfruchtansaat (Untersaat)'  ,date=unter_saat_date ,crop=self))

        
        worksteps.append(WorkStep ('Mähdrusch',date='OKT2',
                                   machine_cost_eur_per_ha=30, diesel_l_per_ha=18,
                                   man_hours_h_per_ha=1.5,crop=self))
        
       
       
        worksteps.append(YieldTransportStep(date='OKT2',crop=self))


        
        
        return worksteps