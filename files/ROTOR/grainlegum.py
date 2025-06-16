from ROTOR.crop import Crop
from ROTOR.crops.data.cropdata import CropData
from ROTOR.covercrop import CoverCrop
from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         
from ROTOR.management.workstep import  HarvestStep, ByproductHarvestStep, DrillStep,SeedBedPreparationStep,YieldTransportStep

from ROTOR.management.fertilizer import FertilizerApplications

from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils.js.jsmodel import ModelFields as MF
from ROTOR.management.workstep import WorkStep,WorkStepList,num_to_date,date_to_num

 
class GrainLegum(Crop ):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fertilizer_applications = FertilizerApplications( model_value_ref = self )
        
        UserEditableModelValue('seed_kg_per_ha',self.get_seed_kg_per_ha,tab = VF.anbau_tab )

        ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)
        UserEditableModelValue('reduced_soil_management',
                               self.get_reduced_soil_management,
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
        
        UserEditableModelValue('spring_striegeln',self.spring_striegeln ,tab=VF.anbau_tab,visible=True, type='bool')
        UserEditableModelValue('do_hacken',self.do_hacken ,tab=VF.anbau_tab,visible=True, type='bool')



        self.primary_tilage_step = PrimaryTilageStep(crop=self, date='OKT1')
        self.reduced_primary_tilage_step =  ReducedPrimaryTilageStep(crop=self ,date='OKT1')
        self.spring_striegel_step = StriegelStep(name='Striegeln', crop=self, date = 'MRZ1' )
        
        self.hack_step = StriegelStep(name='Hacken', crop=self, date = 'APR2',
                                                 machine_cost_eur_per_ha=7.7,
                                                 diesel_l_per_ha= 4,
                                                 man_hours_h_per_ha= 0.55)
 
        self.harvest_step = HarvestStep (crop=self , date='AUG2',  
                                         machine_cost_eur_per_ha= 15,
                                         diesel_l_per_ha= 17,
                                         man_hours_h_per_ha= 0.6)
        
        self.yield_transport_step = YieldTransportStep(crop=self,date='AUG2')
      
    def do_hacken(self):
        return True
    
    def calc_yield_dt_fm_per_ha(self):
        return 30 #  
      
    def autumn_striegeln(self):
        return False
  
    
    def spring_striegeln(self):
        return True

    def calc_byproduct_yield_dt_fm_per_ha(self):
        return self.calc_yield_dt_fm_per_ha() * self.crop_data.hnv_ratio

    def autumn_fertelizer_application(self):
        return False
    
    def supports_undersowing(self):
        return True

    def get_supplies(self):
        supplies = super().get_supplies()
        if not self.fertilizer_applications.isEmpty():
            N,P,K = self.fertilizer_applications.get_NPK_from_fert_kg_per_ha()
            menge = self.fertilizer_applications.get_amount_t_per_ha()
            supplies.append( {MF.supply_name: MF.fertilizer_supply,  'N':N, 'P':P, 'K':K , MF.supply_info: f"{menge} t/ha" } )
            
        return supplies
        
    def get_removals(self):
        removals = super().get_removals()
        N = self.calc_yield_dt_fm_per_ha() * self.get_primary_product_nitrogen_kg_per_dt()
        P = self.calc_yield_dt_fm_per_ha() * self.crop_data.primary_product.phosphate_oxide_kg_per_dt * 0.4364
        K = self.calc_yield_dt_fm_per_ha() * self.crop_data.primary_product.potassium_oxide_kg_per_dt * 0.83 
        removals.append( {MF.removal_name : MF.primary_harvest_removal, 'N':-N, 'P':-P, 'K':-K , MF.removal_info: "-"})
        return removals

    def get_worksteps(self):
        worksteps = []
        
        fertilizer_automn_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=True, for_spring=False)
        fertilizer_spring_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=False, for_spring=True)
    
        if fertilizer_automn_t_per_ha > 0:
            worksteps.append( FertilizerStep(date='OKT1' ,crop=self) ) 
        if fertilizer_spring_t_per_ha > 0:
            worksteps.append( FertilizerStep(date='MRZ2' ,crop=self) )

        if self.has_cover_crop():

            self.primary_tilage_step.date='MRZ2'

            
            if self.cover_crop.get_cultivation() == 'BLANK_SAAT':
                worksteps.append( WorkStep(name='Zwischenfruchtansaat (Blank)' ,date='SEP2' ,crop=self))
                
            if self.cover_crop.get_cultivation() == 'STOPPEL_SAAT':
                worksteps.append( WorkStep(name='Zwischenfruchtansaat (Stoppel)'  ,date='SEP2',crop=self))
                
            if self.cover_crop.get_cover_crop_harvest():
                worksteps.append( WorkStep(name='Zwischenfruchtabfuhr' ,date='MRZ2',crop=self))

        
        if self.get_reduced_soil_management():
            self.reduced_primary_tilage_step.date = self.primary_tilage_step.date
            worksteps.append( self.reduced_primary_tilage_step)
        else:
            worksteps.append( self.primary_tilage_step)

                

        worksteps.append( self.seed_bed_preparation_step )
        worksteps.append( self.drill_step)
        
        if self.autumn_striegeln():
            worksteps.append( self.autumn_striegel_step)
        
        
        if self.spring_striegeln():
            worksteps.append( self.spring_striegel_step)
            
            
        if hasattr(self, 'hack_step'):
            
            if self.do_hacken():
                worksteps.append(self.hack_step)

        if self.next_crop:
            self.next_crop.post_init()
            if self.next_crop.has_cover_crop():
                if self.next_crop.cover_crop.get_cultivation() == 'UNTER_SAAT':
                    unter_saat_date = 'APR1'
                    worksteps.append( WorkStep(name='Zwischenfruchtansaat (Untersaat)'  ,date=unter_saat_date ,crop=self))
            if self.next_crop.crop_data.crop_code == 'LEG_GRAS':
                if self.next_crop.get_cultivation() == 'UNTER_SAAT':
                    unter_saat_date = 'APR2'
                    worksteps.append( WorkStep(name='Leguminosengrasansaat (Untersaat)'  ,date=unter_saat_date ,crop=self))
        
        worksteps.append( self.harvest_step)
        worksteps.append( self.yield_transport_step)

        
        return worksteps
        

class SummerGrainLegum( GrainLegum ):

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        

        UserEditableModelValue('has_cover_crop',self.has_cover_crop ,tab=VF.anbau_tab,visible=True, type='bool')
        

        self.drill_step = DrillStep(crop=self,date='MRZ1')
        self.seed_bed_preparation_step = SeedBedPreparationStep(crop=self,date='MRZ1')

    
    def post_init(self):
        """ should be called after __init__ and when ffolge is complete """
        
        
        if self.has_cover_crop():
            self.cover_crop = CoverCrop( ffelement = self , model_value_ref=self )
            # self.cover_crop_economy = CoverCropEconomy(ffelement=self, model_value_ref = self)

        super().post_init()
        


    def get_cover_crop(self):
        return self.cover_crop

    
    

        

class WinterGrainLegum(GrainLegum):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
        UserEditableModelValue('autumn_striegeln',self.autumn_striegeln ,tab=VF.anbau_tab,visible=True, type='bool')


        self.drill_step = DrillStep(crop=self,date='OKT2')
        self.seed_bed_preparation_step = SeedBedPreparationStep(crop=self,date='OKT2')


    def autumn_striegeln(self):
        return True