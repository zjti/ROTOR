class VDLUFA:

    
    HP_HÄ_per_ha = 0
    NP_HÄ_per_ha = 0
    pp_bp_ratio = 1

    primary_product_yield_dt_fm_per_ha = 100
    
    def __init__(self, 
                 primary_product_yield_dt_fm_per_ha = None, 
                 by_product_yield_dt_fm_per_ha = None,
                 by_product_residual_fraction=1):
        
        self.by_product_residual_fraction = by_product_residual_fraction
        
        if primary_product_yield_dt_fm_per_ha:
            self.primary_product_yield_dt_fm_per_ha = primary_product_yield_dt_fm_per_ha
        if by_product_yield_dt_fm_per_ha is None:
            self.by_product_yield_dt_fm_per_ha = self.primary_product_yield_dt_fm_per_ha * self.pp_bp_ratio 
        else:
            self.by_product_yield_dt_fm_per_ha  = by_product_yield_dt_fm_per_ha
        
    def get_humus_equivalent_hä_per_ha(self):
        return self.get_HP_humus_equivalent_hä_per_ha() + self.get_NP_humus_equivalent_hä_per_ha()

    
    def get_HP_humus_equivalent_hä_per_ha(self):
        return self.HP_HÄ_per_ha 

    def get_NP_humus_equivalent_hä_per_ha(self):
        return self.NP_HÄ_per_ha * self.by_product_yield_dt_fm_per_ha * self.by_product_residual_fraction


    def get_DUNG_humus_equivalent_hä_per_ha(self):
        pass

        
        