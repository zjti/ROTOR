from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.economy.economy import Economy
from ROTOR.management.workstep import WorkStep, WorkStepList

from ROTOR.utils.js.jsmodel import VisFields as VF

class CoverCropEconomy( Economy ):

    def __init__(self, cover_crop_seeds_kg_per_ha=200, cover_crop_seed_cost_eur_per_kg=19, *args, **kwargs):
        super().__init__( *args, **kwargs,model_value_group_name='covercropeconomy')

        self.cover_crop_seeds_kg_per_ha = cover_crop_seeds_kg_per_ha
        self.cover_crop_seed_cost_eur_per_kg = cover_crop_seed_cost_eur_per_kg
        
        UserEditableModelValue('get_cover_crop_seeds_kg_per_ha',self.get_cover_crop_seeds_kg_per_ha ,tab=VF.eco_tab )
        UserEditableModelValue('get_cover_crop_seed_cost_eur_per_kg',self.get_cover_crop_seed_cost_eur_per_kg ,tab=VF.eco_tab )
        ModelValue('get_cover_crop_seed_cost_eur_per_ha', self.get_cover_crop_seed_cost_eur_per_ha, tab=VF.eco_tab )

        # self.worksteps =[]
        # self.worksteplist =  WorkStepList(min_date='AUG1',max_date='APR1', model_value_ref = self)


        # if self.ffelement.cover_crop.get_cultivation() == 'BLANK_SAAT':
        #     self.worksteps += [WorkStep(name='Ansaat (BLANK)', ffelement = self.ffelement , model_value_ref = self.worksteplist ,date='SEP2')]

        # if self.ffelement.cover_crop.get_cultivation() == 'STOPPEL_SAAT':
        #     self.worksteps += [WorkStep(name='Ansaat (STOPPEL)', ffelement = self.ffelement , model_value_ref = self.worksteplist ,date='SEP2')]

        # if self.ffelement.cover_crop.get_cultivation() == 'UNTER_SAAT':
        #     self.worksteps += [WorkStep(name='Ansaat (UNTER)', ffelement = self.ffelement , model_value_ref = self.worksteplist ,date='SEP2')]

        # if self.ffelement.get_reduced_soil_management():
        #     self.worksteps += [WorkStep(name='Einarbeitung  (reduziert)', ffelement = self.ffelement , model_value_ref = self.worksteplist ,date='FEB2')]
        # else:    
        #     self.worksteps += [WorkStep(name='Einarbeitung', ffelement = self.ffelement , model_value_ref = self.worksteplist ,date='FEB2')]

        
        # self.worksteplist.set_worksteps(self.worksteps)
        
        
    def get_cover_crop_seeds_kg_per_ha(self):
        return self.cover_crop_seeds_kg_per_ha
        
    def get_cover_crop_seed_cost_eur_per_kg(self):
        return self.cover_crop_seed_cost_eur_per_kg

    def get_cover_crop_seed_cost_eur_per_ha(self):
        return self.get_cover_crop_seeds_kg_per_ha() * self.get_cover_crop_seed_cost_eur_per_kg()

    