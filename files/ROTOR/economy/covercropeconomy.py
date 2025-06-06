from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.utils.modelvalue import ClassWithModelValues

from ROTOR.management.workstep import WorkStep, WorkStepList

from ROTOR.utils.js.jsmodel import VisFields as VF

class CoverCropEconomy(  ClassWithModelValues ):

    def __init__(self, cover_crop_seeds_kg_per_ha=150, cover_crop_seed_cost_eur_per_kg=0.9, *args, **kwargs):
        super().__init__( *args, **kwargs,model_value_group_name='covercropeconomy')

        self.cover_crop_seeds_kg_per_ha = cover_crop_seeds_kg_per_ha
        self.cover_crop_seed_cost_eur_per_kg = cover_crop_seed_cost_eur_per_kg
        
        UserEditableModelValue('cover_crop_seed_kg_per_ha',self.get_cover_crop_seed_kg_per_ha ,tab=VF.eco_tab )
        UserEditableModelValue('cover_crop_seed_cost_eur_per_kg',self.get_cover_crop_seed_cost_eur_per_kg ,tab=VF.eco_tab )
        ModelValue('cover_crop_seed_cost_eur_per_ha', self.get_cover_crop_seed_cost_eur_per_ha, tab=VF.eco_tab )

      
    def get_cover_crop_seed_kg_per_ha(self):
        return self.cover_crop_seeds_kg_per_ha
        
    def get_cover_crop_seed_cost_eur_per_kg(self):
        return self.cover_crop_seed_cost_eur_per_kg

    def get_cover_crop_seed_cost_eur_per_ha(self):
        return self.get_cover_crop_seed_kg_per_ha() * self.get_cover_crop_seed_cost_eur_per_kg()

    