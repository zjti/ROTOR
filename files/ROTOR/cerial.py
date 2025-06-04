from ROTOR.crop import Crop
from ROTOR.crops.data.cropdata import CropData
from ROTOR.covercrop import CoverCrop
from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue

from ROTOR.economy.covercropeconomy import CoverCropEconomy
from ROTOR.management.fertilizer import FertilizerApplications

from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils.js.jsmodel import ModelFields as MF
from ROTOR.management.workstep import WorkStep,WorkStepList
 
class Cerial(Crop ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fertilizer_applications = FertilizerApplications( model_value_ref = self )
        
        ModelValue('dung_herbst', self.autumn_fertelizer_application, tab = VF.dung_tab, visible=False)
        UserEditableModelValue('reduced_soil_management',
                               self.get_reduced_soil_management,
                               type='bool', tab = VF.anbau_tab )
        
        UserEditableModelValue('byproduct_harvest',
                               self.get_byproduct_harvest,
                               type='bool', tab = VF.anbau_tab )
        
       
        
        

    def autumn_fertelizer_application(self):
        return True
    
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
        removals.append( {MF.removal_name : MF.primary_harvest_removal, 'N':N, 'P':P, 'K':K , MF.removal_info: "-"})
        return removals

    def mk_economy_worksteps(self):
        steps = []
        worksteplist = WorkStepList(model_value_ref=self)
        self.worksteplist = worksteplist

        fertilizer_automn_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=True, for_spring=False)
        fertilizer_spring_t_per_ha = self.fertilizer_applications.get_amount_t_per_ha(for_autumn=False, for_spring=True)
        if fertilizer_automn_t_per_ha > 0:
            worksteplist.add( WorkStep(name=f'Düngerausbringen ({fertilizer_automn_t_per_ha} t/ha)' ,date='SEP2'))
        if fertilizer_spring_t_per_ha > 0:
            worksteplist.add( WorkStep(name=f'Düngerausbringen ({fertilizer_spring_t_per_ha} t/ha)' ,date='MRZ1'))

        soil_management_date = 'OKT2'

        if self.has_cover_crop():
            soil_management_date = 'MRZ2'
            if self.cover_crop.get_cultivation() == 'BLANK_SAAT':
                worksteplist.add( WorkStep(name='Zwischenfruchtansaat (Blank)' ,date='SEP2'))
                
            if self.cover_crop.get_cultivation() == 'STOPPEL_SAAT':
                worksteplist.add( WorkStep(name='Zwischenfruchtansaat (Stoppel)'  ,date='SEP2'))

            if self.cover_crop.get_cover_crop_harvest():
                worksteplist.add( WorkStep(name='Zwischenfruchtabfuhr' ,date='MRZ2'))

        
        
        if self.get_reduced_soil_management():
            worksteplist.add( WorkStep(name='Bodenbearbeitung (Reduziert)' ,date=soil_management_date))
        else:
            worksteplist.add( WorkStep(name='Bodenbearbeitung' ,date=soil_management_date))
            
                

        worksteplist.add( WorkStep(name='Ansaat' ,date='MRZ2'))
        
        worksteplist.add( WorkStep(name='Pflege' ,date='APR2'))

        worksteplist.add( WorkStep(name='Ernte + Lagern' ,date='AUG1'))

        if self.get_byproduct_harvest():
            worksteplist.add( WorkStep(name='Strohernte' ,date='AUG2'))

        
        
        
        

        
            
        

        

class SummerCerial( Cerial ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        UserEditableModelValue('has_cover_crop',self.has_cover_crop ,tab=VF.anbau_tab,visible=True, type='bool')

    def post_init(self):
        """ should be called after __init__ and when ffolge is complete """
        
        if self.has_cover_crop():
            self.cover_crop = CoverCrop( ffelement = self , model_value_ref=self )
            self.cover_crop_economy = CoverCropEconomy(ffelement=self, model_value_ref = self)

        super().post_init()

    def get_cover_crop(self):
        return self.cover_crop
    

        

class WinterCerial( Cerial ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

