from ROTOR.utils.modelvalue import ClassWithModelValues
from ROTOR.economy.covercropeconomy import CoverCropEconomy

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import WorkStep, WorkStepList
from ROTOR.utils.js.jsmodel import VisFields as VF

class FFEconomy( ClassWithModelValues ):

    def __init__(self, crop=None, *args,**kwargs):
        super().__init__(*args,**kwargs,model_value_group_name='economy')
        UserEditableModelValue('diesel_eur_per_l',self.get_diesel_eur_per_l ,tab=VF.eco_tab )
        UserEditableModelValue('extra_cost_eur_per_ha',self.get_extra_cost_eur_per_ha ,tab=VF.eco_tab )
    
    def get_diesel_eur_per_l(self):
        return 1.7

    def get_extra_cost_eur_per_ha(self):
        return 50


class CropEconomy( ClassWithModelValues ):
    """
    Grundbodenbearbeitung (Pflug),28.1,1.4,20
    Saatbettbereitung (Saatbettkombi)	,7.9,0.32,5
    Drillen (Kreiselegge+Sämaschine)	,19.5,0.9,8
    Walzen Saatbett/Ansaat	,4.7,0.34,3.5
    Mineraldünger streuen 1)	,1.5,0.17,1.5
    Mähdrusch Getreide	14.3,0.54,16
    Erntegut abfahren (5 km) 5.1,0.34,5.1
    Stroh pressen Hilfe	,28.5,0.22,2
    Stroh auf-/abladen, abfahren (5 km) Hilfe	,7.2,0.62,6
    Bodenbearbeitung (Grubber)	,8.1,0.46,6.2
    """

    
    def __init__(self, crop=None, *args,**kwargs):
        super().__init__(*args,**kwargs,model_value_group_name='cropeconomy')

        if crop.has_cover_crop():
            self.cover_crop_economy = CoverCropEconomy( model_value_ref = self)
        
        self.crop = crop
        self.seed_kg_per_ha = crop.seed_kg_per_ha
        self.seed_cost_eur_per_kg = crop.seed_cost_eur_per_kg
        
        # UserEditableModelValue('get_seed_kg_per_ha',self.get_seed_kg_per_ha ,tab=VF.eco_tab )
        # self.modelvalue_seed_kg_per_ha = crop.modelvalue_seed_kg_per_ha
        UserEditableModelValue('seed_cost_eur_per_kg',self.get_seed_cost_eur_per_kg ,tab=VF.eco_tab , unit = '€/kg' )
        ModelValue('seed_cost_eur_per_ha', self.get_seed_cost_eur_per_ha, tab=VF.eco_tab ,unit = '€/ha' )
        UserEditableModelValue('price_yield_eur_per_dt_fm', self.get_price_yield_eur_per_dt_fm, tab=VF.eco_tab , unit = '€/dt')
        UserEditableModelValue('extra_cost_eur_per_ha',self.get_extra_cost_eur_per_ha ,tab=VF.eco_tab ,unit = '€/ha' )

        ModelValue('yield_leistung_eur_per_ha', self.get_yield_leistung_eur_per_ha, tab=VF.eco_tab , unit = '€/ha')

        ModelValue('sum_leistung_eur_per_ha', self.get_sum_leistung_eur_per_ha, tab=VF.eco_tab , unit = '€/ha')
        ModelValue('sum_machine_cost_eur_per_ha', self.get_sum_machine_cost_eur_per_ha, tab=VF.eco_tab , unit = '€/ha')
        ModelValue('sum_diesel_cost_eur_per_ha', self.get_sum_diesel_cost_eur_per_ha, tab=VF.eco_tab , unit = '€/ha' )
        UserEditableModelValue('other_leistung_eur_per_ha', self.get_other_leistung_eur_per_ha, tab=VF.eco_tab , unit = '€/ha' ) 

        ModelValue('sum_man_hours_per_ha', self.get_sum_man_hours_per_ha, tab=VF.eco_tab , unit = 'AKh/ha' )
        ModelValue('gross_margin_eur_per_ha', self.get_gross_margin_eur_per_ha, tab=VF.eco_tab , unit = '€/ha' )
        ModelValue('gross_margin_per_man_hour_eur_per_h', self.get_gross_margin_per_man_hour_eur_per_h, tab=VF.eco_tab , unit = '€/AKh' )
        
        worksteplist = WorkStepList(model_value_ref=self)
        self.worksteplist = worksteplist

        for step in crop.get_worksteps():
            worksteplist.add(step)


    def get_gross_margin_per_man_hour_eur_per_h(self):
        try:
            return self.get_gross_margin_eur_per_ha() / self.get_sum_man_hours_per_ha()
        except:
            return 0
    
    def get_gross_margin_eur_per_ha(self):
        M = self.get_sum_leistung_eur_per_ha() 
        M -= self.get_sum_diesel_cost_eur_per_ha()
        M -= self.get_extra_cost_eur_per_ha()
        M -= self.get_sum_machine_cost_eur_per_ha() 
        M -= self.get_seed_cost_eur_per_ha()
        if self.crop.has_cover_crop():
            M -= self.cover_crop_economy.get_cover_crop_seed_cost_eur_per_ha()
        return M
    
    def get_yield_leistung_eur_per_ha(self):
        return self.get_price_yield_eur_per_dt_fm() * self.crop.calc_yield_dt_fm_per_ha()
        
    def get_sum_leistung_eur_per_ha(self):
        return self.get_other_leistung_eur_per_ha() + self.get_yield_leistung_eur_per_ha()
        
    def get_sum_diesel_cost_eur_per_ha(self):
        S=0
        for workstep in self.worksteplist.worksteps:
            S+= workstep.get_diesel_eur_per_ha()
        return S
    
    def get_sum_man_hours_per_ha(self):
        S=0
        for workstep in self.worksteplist.worksteps:
            S+= workstep.get_man_hours_h_per_ha()
        return S
    
    def get_sum_machine_cost_eur_per_ha(self):
        S=0
        for workstep in self.worksteplist.worksteps:
            S+= workstep.get_machine_cost_eur_per_ha()
        return S
        
    def get_extra_cost_eur_per_ha(self):
        return self.crop.ff_economy.get_extra_cost_eur_per_ha()
        
    def get_price_yield_eur_per_dt_fm(self):
        return self.crop.price_yield_eur_per_dt_fm
      
    def get_seed_cost_eur_per_kg(self):
        return self.seed_cost_eur_per_kg

    def get_seed_cost_eur_per_ha(self):
        return self.crop.get_seed_kg_per_ha() * self.get_seed_cost_eur_per_kg()

    def get_other_leistung_eur_per_ha(self):
        return 0

        