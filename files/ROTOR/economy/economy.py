import json
from ROTOR.utils.modelvalue import ClassWithModelValues
from ROTOR.economy.covercropeconomy import CoverCropEconomy

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import WorkStep, WorkStepList, date_to_num
from ROTOR.utils.js.jsmodel import VisFields as VF
from ROTOR.utils import config
 
class FFEconomy( ClassWithModelValues ):

    def __init__(self, ffolge, *args,**kwargs):
        
        super().__init__(*args,**kwargs,model_value_group_name='economy')
        UserEditableModelValue('diesel_eur_per_l',self.get_diesel_eur_per_l ,tab=VF.eco_tab )
        UserEditableModelValue('sesssion_labour_eur_per_h',self.get_sesssion_labour_eur_per_h ,tab=VF.eco_tab )
        UserEditableModelValue('extra_cost_eur_per_ha',self.get_extra_cost_eur_per_ha ,tab=VF.eco_tab )
        
        UserEditableModelValue('diesel_faktor',self.get_diesel_faktor ,tab=VF.eco_tab )
        UserEditableModelValue('manhour_faktor',self.get_manhour_faktor ,tab=VF.eco_tab )
        UserEditableModelValue('machinecost_faktor',self.get_machinecost_faktor ,tab=VF.eco_tab )

        ModelValue('ff_gross_margin_eur_per_ha', self.get_ff_gross_margin_eur_per_ha, unit = '€/ha')
        
        ModelValue('arbeits_spitzen_plot', self.get_arbeits_spitzen_plot)
        ModelValue('half_months',self.get_half_months)
        
        self.ffolge=ffolge
        
    def get_half_months(self):
        return [
            'JAN1','JAN2','FEB01','FEB2','MRZ1','MRZ2',
            'APR1','APR2','MAI1','MAI2','JUN1','JUN2',
            'JUL1','JUL2','AUG1','AUG2','SEP1','SEP2',
            'OKT1','OKT2','NOV1','NOV2','DEZ1','DEZ2',
        ] 
        
    def get_arbeits_spitzen_plot(self):
        baseColors = [
            '#1abc9c', '#3498db', '#e67e22', '#e74c3c',
            '#9b59b6', '#f1c40f', '#2ecc71', '#34495e'
        ]
        plts = []
        for i,crop in enumerate(self.ffolge.crops):
            if crop:
                if hasattr(crop,'economy'):
                    data = [0 for i in range(24)]
                    for ws in crop.economy.worksteplist.worksteps:
                        print('x1x',ws)
                        data[date_to_num[ws.get_date()]] += ws.get_man_hours_h_per_ha()
                        
                    plt = {
                        'label': crop.crop_data.crop_code,
                        'data': data,
                        'backgroundColor': baseColors[i % len(baseColors)],
                        'stack': 'stack-0'
                    }
                    plts+=[plt]
        
        return plts
        
    def get_ff_gross_margin_eur_per_ha(self):
        S,N=0,0
        for crop in self.ffolge.crops:
            if crop:
                if hasattr(crop,'economy'):
                    S += crop.economy.get_gross_margin_eur_per_ha()
                    N += 1
        try:
            return S/N
        except:
            return 0
        
    def get_diesel_eur_per_l(self):
        return 1.7

    def get_extra_cost_eur_per_ha(self):
        return 50
    
    def get_sesssion_labour_eur_per_h(self):
        return 13
    
    def get_diesel_faktor(self):
        if config.PARAMS_USER['FARMSIZE']['default']  == 'FARM_SMALL':
            return 1.1
        if config.PARAMS_USER['FARMSIZE']['default']  == 'FARM_BIG':
            return 0.9
        return 1
    
    def get_manhour_faktor(self):
        if config.PARAMS_USER['FARMSIZE']['default']  == 'FARM_SMALL':
            return 1.1
        if config.PARAMS_USER['FARMSIZE']['default']  == 'FARM_BIG':
            return 0.9
        return 1
    
    def get_machinecost_faktor(self):
        # print('fs',config.PARAMS_USER['FARMSIZE'])
        if config.PARAMS_USER['FARMSIZE']['default'] == 'FARM_SMALL':
            return 1.1
        if config.PARAMS_USER['FARMSIZE']['default']  == 'FARM_BIG':
            return 0.9
        return 1
    
    def write_report(self):
        from ROTOR.economy.economy_report import EconomyReport
        report = EconomyReport(self.ffolge).get_report_bytes()
        return report


class CropEconomy( ClassWithModelValues ):
     
    def __init__(self, crop=None, *args,**kwargs):
        super().__init__(*args,**kwargs,model_value_group_name='cropeconomy')

        if crop.has_cover_crop():
            self.cover_crop_economy = CoverCropEconomy( model_value_ref = self)
        
        self.crop = crop
        self.seed_kg_per_ha = crop.seed_kg_per_ha
        self.seed_cost_eur_per_kg = crop.seed_cost_eur_per_kg
        
        # UserEditableModelValue('get_seed_kg_per_ha',self.get_seed_kg_per_ha ,tab=VF.eco_tab )
        # self.modelvalue_seed_kg_per_ha = crop.modelvalue_seed_kg_per_ha
        if hasattr(self.crop , 'seed_u_per_ha'):
            UserEditableModelValue('seed_cost_eur_per_u',self.get_seed_cost_eur_per_u ,tab=VF.eco_tab , unit = '€/U' )
        else:
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
        
        ModelValue('fertilizer_cost_eur_per_ha', self.get_fertilizer_cost_eur_per_ha, tab=VF.eco_tab , unit = '€/ha' )
        
        worksteplist = WorkStepList(model_value_ref=self)
        self.worksteplist = worksteplist

        for step in crop.get_worksteps():
            worksteplist.add(step)


    def get_gross_margin_per_man_hour_eur_per_h(self):
        try:
            return self.get_gross_margin_eur_per_ha() / self.get_sum_man_hours_per_ha()
        except:
            return 0
        
    
        
    def get_fertilizer_cost_eur_per_ha(self):
        M = 0
        if not hasattr(self.crop,'fertilizer_applications'):
            return 0
        
        fertelizer_application  = self.crop.fertilizer_applications
        for dung_key,dung_val in fertelizer_application.get_dung_menge().items():
            dung_param = config.DUNG_DATA[dung_key]

            M += dung_val['menge'] * dung_param['PREIS_EUR_PER_T']
        return M
        
    def get_sum_cost_eur_per_ha(self):
        S = 0
        
        S+= self.get_sum_machine_cost_eur_per_ha()
        S+= self.get_sum_diesel_cost_eur_per_ha()
        S+= self.get_seed_cost_eur_per_ha()
        if self.crop.has_cover_crop():
            S+= self.cover_crop_economy.get_cover_crop_seed_cost_eur_per_ha()
        
        S+= self.get_fertilizer_cost_eur_per_ha() 
        S+= self.get_extra_cost_eur_per_ha() 
        
        return S
    
    def get_gross_margin_eur_per_ha(self):
        M = self.get_sum_leistung_eur_per_ha() 
        M -= self.get_sum_cost_eur_per_ha()
        
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
    
    def get_seed_cost_eur_per_u(self):
        return self.crop.seed_cost_eur_per_u

    def get_seed_cost_eur_per_ha(self):
        if hasattr(self.crop, 'get_seed_u_per_ha'):
            return  self.crop.get_seed_u_per_ha() * self.get_seed_cost_eur_per_u() 
        else:
            return self.crop.get_seed_kg_per_ha() * self.get_seed_cost_eur_per_kg()
    


    def get_other_leistung_eur_per_ha(self):
        return 0

    
        