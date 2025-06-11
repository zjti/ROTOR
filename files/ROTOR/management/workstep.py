from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue,ClassWithModelValues
from ROTOR.utils.js.jsmodel import VisFields as VF

all_dates = [
    'JAN1','JAN2','FEB01','FEB2','MRZ1','MRZ2',
    'APR1','APR2','MAI1','MAI2','JUN1','JUN2',
    'JUL1','JUL2','AUG1','AUG2','SEP1','SEP2',
    'OKT1','OKT2','NOV1','NOV2','DEZ1','DEZ2',
]

date_to_num = {date:i for i,date in  enumerate(all_dates)}
num_to_date = {i:date for i,date in enumerate(all_dates)}

def get_date_range(min_date,max_date):
    num_min_date = date_to_num[min_date]
    date_range = []
    for i in range(24):
        date_range += [ num_to_date[ (i + num_min_date)%24 ] ]
        if date_range[-1] == max_date:
            break
    return date_range

class WorkStepList ( ClassWithModelValues ):
    """
        * this sets min_date and max_date of all elemnts in work_steps.
    """
    def __init__(self, *args,  min_date='JAN1', max_date='DEZ2',  **kwargs):
        super().__init__(*args, **kwargs, model_value_group_name='worksteplist')

        self.min_date=min_date
        self.max_date=max_date

        self.worksteps=[]

    def add(self, workstep):

        # # TODO: this could be improved by overwrite setter to _model_values
        # if workstep._model_values is None:
        #     workstep._model_values = self._model_values 
        #     workstep._model_value_ref = self
        #     setattr(self, '_model_child_'+str(id(workstep)), workstep)

        new_workstep = WorkStep( workstep.name, workstep.date, workstep.machine_cost_eur_per_ha,
                                 workstep.man_hours_h_per_ha, workstep.diesel_l_per_ha, workstep.crop, model_value_ref =self  )

        self.worksteps.append(new_workstep)
    
    def set_worksteps(self, work_steps):
        for i,work_step in enumerate(work_steps):
            work_step.min_date = self.min_date
            work_step.max_date = self.max_date

            if i > 0:
                work_step.min_date = work_steps[i-1].get_date()
            if i < len(work_steps)-1:
                work_step.max_date = work_steps[i+1].get_date()
                
            

class WorkStep( ClassWithModelValues ):

    def __init__(self, name, date = 'JAN1', machine_cost_eur_per_ha=12 , man_hours_h_per_ha=0.6, diesel_l_per_ha= 4.5, crop = None, *args, **kwargs):
        super().__init__(*args, **kwargs,  model_value_group_name=name)
        
        self.name = name
        self.date = date
        self.diesel_l_per_ha = diesel_l_per_ha
        self.machine_cost_eur_per_ha = machine_cost_eur_per_ha
        self.man_hours_h_per_ha = man_hours_h_per_ha
        self.crop = crop
        # UserEditableModelValue(name +'_get_date', self.get_date, tab=VF.eco_workstep_tab, type='date' )
        UserEditableModelValue('get_date', self.get_date, type='select', select_opts = self.get_date_options )
        UserEditableModelValue('get_man_hours_h_per_ha', self.get_man_hours_h_per_ha )
        UserEditableModelValue('get_diesel_l_per_ha', self.get_diesel_l_per_ha )
        UserEditableModelValue('get_machine_cost_eur_per_ha', self.get_machine_cost_eur_per_ha )

        ModelValue('get_diesel_eur_per_ha', self.get_diesel_eur_per_ha, unit = '€/l' )



    def get_date_options(self):
        if (hasattr(self,'min_date') and hasattr(self,'max_date') and
            self.min_date and self.max_date):
            
            return get_date_range(self.min_date,self.max_date)
        return all_dates
        
    def get_date(self):
        return self.date

    def get_man_hours_h_per_ha(self):
        return self.man_hours_h_per_ha

    def get_diesel_l_per_ha(self):
        return self.diesel_l_per_ha

    
    def get_diesel_eur_per_ha(self):
        return self.get_diesel_l_per_ha() * self.crop.ff_economy.get_diesel_eur_per_l()

    def get_machine_cost_eur_per_ha(self):
        return self.machine_cost_eur_per_ha


class PrimaryTilageStep(WorkStep):
    def __init__(self,name="Grundbodenbearbeitung", date = 'OKT1', machine_cost_eur_per_ha= 28.1 , man_hours_h_per_ha=1.4, diesel_l_per_ha=20,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)

class ReducedPrimaryTilageStep(WorkStep):
    def __init__(self,name="Grundbodenbearbeitung (Reduziert)", date = 'OKT1', machine_cost_eur_per_ha= 18.1 , man_hours_h_per_ha=0.8, diesel_l_per_ha=11,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)


class SeedBedPreparationStep(WorkStep):
    def __init__(self,name="Saatbettbereitung", date = 'OKT2', machine_cost_eur_per_ha= 7.9 , man_hours_h_per_ha= 0.4, diesel_l_per_ha=5,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)

class DrillStep(WorkStep):
    def __init__(self,name="Drillen", date = 'OKT2', machine_cost_eur_per_ha= 19.5 , man_hours_h_per_ha= 0.9, diesel_l_per_ha=8,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)

class StriegelStep(WorkStep):
    def __init__(self,name="Striegeln", date = 'OKT2', machine_cost_eur_per_ha= 4.5 , man_hours_h_per_ha= 0.23, diesel_l_per_ha=3,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)


class HarvestStep(WorkStep):
    def __init__(self,name="Mähdrusch", date = 'OKT2', machine_cost_eur_per_ha= 14.3 , man_hours_h_per_ha= 0.54, diesel_l_per_ha=16,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)

class YieldTransportStep(WorkStep):
    def __init__(self,name="Erntegut abfahren", date = 'OKT2', machine_cost_eur_per_ha= 14.3 , man_hours_h_per_ha= 0.54, diesel_l_per_ha=16,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)

class ByproductHarvestStep(WorkStep):
    def __init__(self,name="Strohernte", date = 'OKT2', machine_cost_eur_per_ha= 21.3 , man_hours_h_per_ha= 0.6, diesel_l_per_ha=8,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)


class FertilizerStep(WorkStep):
    def __init__(self,name="Dünger ausbringen", date = 'JAN1', machine_cost_eur_per_ha= 1.5 , man_hours_h_per_ha=0.2, diesel_l_per_ha=1.5,*args, **kwargs):
        super().__init__(name, date, machine_cost_eur_per_ha, man_hours_h_per_ha, diesel_l_per_ha,*args, **kwargs)





        