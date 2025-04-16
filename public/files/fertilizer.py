import config

class FertilizerApplications:
    """
    represents fertilizer applications for a crop.
    """
    def __init__(self):
        self.dung_menge = {}
        
    def get_amount_t_per_ha(self):
        M = 0
        for dung_val in self.dung_menge.values():
            M += dung_val['menge'] 
        return M
    
    def isEmpty(self):
        M = self.get_amount_t_per_ha()
        if M > 0:
            return False
        return True
        
    def deserialize(self, dung_menge):
        self.dung_menge = dung_menge
        
    def get_N_avail_from_fert_kg_per_ha(self):
        N=0
        
        if not self.dung_menge:
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
        
        if not self.dung_menge:
            return (N,P,K)
 
        # {'fest frisch rind': {'menge': 4, 'is_herbst': False}}...
        for dung_key,dung_val in self.dung_menge.items():
            dung_param = config.DUNG_DATA[dung_key]

            N += dung_val['menge'] * dung_param['N/FM'] * ( 100 - dung_param['Nloss'] ) / 100
            P += dung_val['menge'] * dung_param['P/FM']
            K += dung_val['menge'] * dung_param['K/FM']
            
        return (N,P,K)
    
    
    
    
    