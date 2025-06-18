from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue, ClassWithModelValues
from ROTOR.utils import config
from ROTOR.humus import vdlufa04
from ROTOR.humus import repro_dyn
from ROTOR.humus.vdlufa04.vdlufa import VDLUFA
from ROTOR.humus.repro_dyn.repro_base import  ReproBase
import pkgutil
import inspect
from importlib import import_module

def get_crop_humus_dict(humus_type,humus_module):

    
    crop_dict ={}
    # print(list(pkgutil.iter_modules(crops.__path__)))
    # print(os.getcwd())
    for _,module_name,_ in pkgutil.iter_modules(humus_module.__path__):
        
        full_module_name = f"{humus_module.__name__}.{module_name}"
        module = import_module(full_module_name)
        
        # Find all classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                # print(obj, issubclass(obj,Crop),obj,rop)
                if  issubclass(obj, humus_type):
                    crop_dict[name] = obj
    return crop_dict
humus_VDLUFA_dict = get_crop_humus_dict(VDLUFA, vdlufa04)
humus_REPRO_dict = get_crop_humus_dict(ReproBase, repro_dyn)



class FFEval(ClassWithModelValues):
    def __init__(self, ffolge, model_values=None, model_value_ref=None):
        super().__init__(model_values, model_value_ref, model_value_group_name='ff_eval')
        self.ffolge = ffolge
        UserEditableModelValue(f'humus_method',self.get_humus_method, type='select', select_opts=['VDLUFA','REPRO']) 

        
        ModelValue('mean_yield_dt_fm_per_ha',self.mean_yield_dt_fm_per_ha)
        ModelValue('mean_N_fix', self.mean_N_fix)
        ModelValue('mean_N_from_fert',self.mean_N_from_fert)
        ModelValue('mean_N_removal',self.mean_N_removal )
        ModelValue('mean_N_leach',self.mean_N_leach )
        ModelValue('mean_N_balance',self.mean_N_balance )
        
        ModelValue('mean_humus',self.mean_humus )
        ModelValue('mean_P_balance',self.mean_P_balance)
        ModelValue('mean_K_balance',self.mean_K_balance )
        ModelValue('mean_kraut_mj',self.mean_kraut_mj )
        ModelValue('mean_kraut_w',self.mean_kraut_w )
        ModelValue('mean_kraut_s',self.mean_kraut_s )


#          ModelValue('P_balance',self.get_P_balance)
#         ModelValue('K_balance',self.get_K_balance)
#         ModelValue('N_leach',self.calc_N_leaching_kg_per_ha)
        
#         ModelValue('N_fix',self.calc_N_total_fixation_kg_per_ha)
#         ModelValue('N_from_fert',self.get_N_from_fert)
#         ModelValue('N_removal',self.get_N_removal)
        
#         ModelValue('N_uptake',self.get_N_uptake)
#         ModelValue('N_balance',self.get_N_balance)
#         ModelValue('kraut_mj',self.kraut_mj)
#         ModelValue('kraut_w',self.kraut_w)
#         ModelValue('kraut_s',self.kraut_s)



    def mean_kraut_w(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.kraut_w()
        if N > 0:
            return X/N
        return 0     

    def mean_kraut_mj(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.kraut_s()
        if N > 0:
            return X/N
        return 0     


    def mean_kraut_mj(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.kraut_mj()
        if N > 0:
            return X/N
        return 0     

    def mean_K_balance(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.get_K_balance()
        if N > 0:
            return X/N
        return 0     

    def mean_P_balance(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.get_P_balance()
        if N > 0:
            return X/N
        return 0     


    def mean_humus(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.cropeval.get_humus()
        if N > 0:
            return X/N
        return 0     


    def mean_N_balance(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.get_N_balance()
        if N > 0:
            return X/N
        return 0     


    def mean_N_leach(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.calc_N_leaching_kg_per_ha()
        if N > 0:
            return X/N
        return 0        
 
    def mean_N_removal(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.get_N_removal()
        if N > 0:
            return X/N
        return 0
    
    def mean_N_from_fert(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.get_N_from_fert()
        if N > 0:
            return X/N
        return 0
    
    def mean_N_fix(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.calc_N_total_fixation_kg_per_ha()
        if N > 0:
            return X/N
        return 0
    
    
    def mean_yield_dt_fm_per_ha(self):
        X=0
        N=0
        for crop in self.ffolge.crops:
            if crop:
                N+=1
                X+= crop.calc_yield_dt_fm_per_ha()
        if N > 0:
            return X/N
        return 0
    
           
    def get_humus_method(self):
        return 'VDLUFA'
    
    
    
class CropEval (ClassWithModelValues):
    
    def __init__(self, crop  , model_values=None, model_value_ref=None):
        super().__init__(model_values, model_value_ref, model_value_group_name='cropeval')
        
        self.crop = crop
        
        
        ModelValue('humus',self.get_humus)
        
  
    
    
        

    def get_humus(self):
        S = 0
        if self.crop.ff_eval.get_humus_method()=='VDLUFA':
            pp_yield = None
            bp_yield = None
            residual = 1
            
            if hasattr(self.crop, 'calc_yield_dt_fm_per_ha'):
                pp_yield = self.crop.calc_yield_dt_fm_per_ha()
            
            if self.crop.get_byproduct_harvest():
                residual = 0
            
            humusclass =humus_VDLUFA_dict[self.crop.crop_data.crop_code]
            self.vdlufa_humus = humusclass(primary_product_yield_dt_fm_per_ha = pp_yield,
                                            by_product_yield_dt_fm_per_ha= bp_yield ,
                                            by_product_residual_fraction= residual)
            
        
            S += self.vdlufa_humus.get_HP_humus_equivalent_hä_per_ha()
            S += self.vdlufa_humus.get_NP_humus_equivalent_hä_per_ha()
                
            if hasattr(self.crop, 'has_cover_crop'):
                if self.crop.has_cover_crop():
                    if self.cover_crop.get_cultivation() == 'UNTER_SAAT':
                        humusclass =humus_VDLUFA_dict['ZW_UNTER']
                        
                    elif self.cover_crop.get_cultivation() == 'BLANK_SAAT':
                        humusclass =humus_VDLUFA_dict['ZW_BLANK']
                        
                    else:
                        humusclass =humus_VDLUFA_dict['ZW_STOPPEL']
                    h = humusclass()
                    S += h.get_HP_humus_equivalent_hä_per_ha()
                    S += h.get_NP_humus_equivalent_hä_per_ha()
                    
                        
        else:
            humusclass =humus_REPRO_dict[self.crop.crop_data.crop_code]
            ackerzahl = config.SOIL['ACKERZAHL']['default']
            N_imission_kg_per_ha = config.SOIL['N_DEPO']['default']
            total_N_from_fertilizer_kg_per_ha = 0
            N_avail_from_fertilizer_kg_per_ha = 0
            
            seed_kg_per_ha = self.crop.get_seed_kg_per_ha()
            primary_product_yield_dt_fm_per_ha = self.crop.calc_yield_dt_fm_per_ha()
            by_product_yield_dt_fm_per_ha = None
            if hasattr(self.crop, 'calc_byproduct_yield_dt_fm_per_ha'):
                by_product_yield_dt_fm_per_ha = self.crop.calc_byproduct_yield_dt_fm_per_ha()
            
            
            if hasattr(self.crop,'fertilizer_applications'):
                total_N_from_fertilizer_kg_per_ha = self.crop.fertilizer_applications.get_N_total_from_fert_kg_per_ha()
                N_avail_from_fertilizer_kg_per_ha = self.crop.fertilizer_applications.get_N_avail_from_fert_kg_per_ha()
                        
            self.repro : ReproBase = humusclass(total_N_from_fertilizer_kg_per_ha=total_N_from_fertilizer_kg_per_ha,
                                    N_avail_from_fertilizer_kg_per_ha=N_avail_from_fertilizer_kg_per_ha,
                                    N_imission_kg_per_ha=N_imission_kg_per_ha,
                                    seed_kg_per_ha=seed_kg_per_ha, 
                                    primary_product_yield_dt_fm_per_ha = primary_product_yield_dt_fm_per_ha,
                                    by_product_yield_dt_fm_per_ha=by_product_yield_dt_fm_per_ha, 
                                    ackerzahl=ackerzahl)

            S += self.repro.calc_humus_mehrer_leistung() * 580
            S -= self.repro.calc_humus_brutto_need() * 580
            
            if hasattr(self.crop ,'get_byproduct_harvest'):
                if self.crop.get_byproduct_harvest() == False:
                    S += self.repro.calc_humus_ersatz_leistung_residuals() * 580
            
            if hasattr(self.crop, 'has_cover_crop'):
                if self.crop.has_cover_crop():
                    
                    humusclass =humus_REPRO_dict['ZWFRU']
                    zw_repro : ReproBase = humusclass(ackerzahl = ackerzahl, primary_product_yield_dt_fm_per_ha = 80)
                    S += zw_repro.calc_humus_mehrer_leistung() * 580
                    S -= zw_repro.calc_humus_brutto_need() * 580
                    S += zw_repro.calc_humus_ersatz_leistung_residuals() * 580
                    

        
        S += self.crop.fertilizer_applications.get_humus_kg_per_ha()
        
        return S