from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue, ClassWithModelValues
from ROTOR.economy.covercropeconomy import CoverCropEconomy

from ROTOR.utils.js.jsmodel import VisFields as VF


class CoverCrop (ClassWithModelValues):
    def __init__(self, ffelement, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ffelement = ffelement
        
        UserEditableModelValue('get_cnum',self.get_cnum ,tab=VF.anbau_tab,visible=True)
        UserEditableModelValue('get_leguminosen_percentage',self.get_leguminosen_percentage ,tab=VF.anbau_tab,visible=True)
        UserEditableModelValue('get_cultivation',self.get_cultivation ,tab=VF.anbau_tab,visible=True, type='select', select_opts=self.get_cultivation_options )
        UserEditableModelValue('get_winterhardines',self.get_winterhardines ,tab=VF.anbau_tab,visible=True, 
                               type='select', select_opts=self.get_winterhardines_options )

        if self.get_winterhardines() == 'HIGH' :
            UserEditableModelValue('get_cover_crop_harvest',self.get_cover_crop_harvest ,tab=VF.anbau_tab,visible=True, type='bool' )



    def calc_total_N_uptake_kg_per_ha(self):
        return 30
        
    def calc_N_fixation_kg_per_ha(self):
        return 10
    
    def get_cultivation_options(self):
        opts = ['BLANK_SAAT','STOPPEL_SAAT']
        if self.ffelement.pre_crop:
            if self.ffelement.pre_crop.supports_undersowing():
                opts += ['UNTER_SAAT']
        return opts

    def get_cultivation(self):
        return 'BLANK_SAAT'
        
    def get_winterhardines_options(self):
        return ['NOT_HARD','HARD']

    def get_winterhardines(self):
        return 'HARD'

    def get_cover_crop_harvest(self):
        return False
    
    def get_cnum(self):
        return 321

    def get_leguminosen_percentage(self):
        return 13