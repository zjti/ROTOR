from ROTOR.utils import config
from ROTOR.utils.modelvalue import ClassWithModelValues, UserEditableModelValue
from ROTOR.utils.js.jsmodel import  VisFields as VF



class FertilizerApplications(ClassWithModelValues):
    """
    fertilizer applications for a crop.
    """
    def __init__(self, dung_menge=None, *args,**kwargs):
        super().__init__(*args,**kwargs)

        UserEditableModelValue('dung_menge', self.get_dung_menge, tab = VF.dung_tab, visible=False)

        
        if dung_menge is None:
            self.dung_menge = {}
        else :
            self.dung_menge = dung_menge

            
        
    def get_amount_t_per_ha(self, for_autumn= True, for_spring=True):
        M = 0
        for dung_val in self.get_dung_menge().values():
            if dung_val['is_herbst'] and for_autumn:
                M += dung_val['menge'] 
            if dung_val['is_herbst'] == False and for_spring:
                M += dung_val['menge'] 
        return M

    def get_dung_menge(self):
        return self.dung_menge
    
    def isEmpty(self):
        M = self.get_amount_t_per_ha()
        if M > 0:
            return False
        return True
        
    def deserialize(self, dung_menge):
        self.dung_menge = dung_menge
        
    def get_N_avail_from_fert_kg_per_ha(self):
        N=0
        
        if not self.get_dung_menge():
            return N
 
        # {'fest frisch rind': {'menge': 4, 'is_herbst': False}}...
        for dung_key,dung_val in self.dung_menge.items():
            dung_param = config.DUNG_DATA[dung_key]

            N += dung_val['menge'] * dung_param['N/FM'] * ( 100 - dung_param['Nloss'] ) / 100
            #Navil_spring': 20, 'Navil_autumn': 20
            if dung_val['is_herbst']:
                N *= dung_param['Navil_autumn'] / 100
            if dung_val['is_herbst']:
                N *= dung_param['Navil_spring'] / 100
            
        return N
    
    def get_NPK_from_fert_kg_per_ha(self):
        N,P,K = 0,0,0
        
        if not self.get_dung_menge():
            return (N,P,K)
 
        # {'fest frisch rind': {'menge': 4, 'is_herbst': False}}...
        for dung_key,dung_val in self.get_dung_menge().items():
            dung_param = config.DUNG_DATA[dung_key]

            N += dung_val['menge'] * dung_param['N/FM'] * ( 100 - dung_param['Nloss'] ) / 100
            P += dung_val['menge'] * dung_param['P/FM']
            K += dung_val['menge'] * dung_param['K/FM']
            
        return (N,P,K)
    
    
    
    
    