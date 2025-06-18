from ROTOR.humus.repro_dyn.repro_base import  ReproHumusMehrer

class ZWFRU( ReproHumusMehrer):
    
    std_bilanz_coefficent = 0.3
    
    pp_bp_ratio = 0
    bp_pp_ratio = 0 #  by_product_yield_dt_fm / primary_product_yield_dt_fm 
    N_content_seed_kg_per_kg = 0.03
    N_content_by_product_kg_per_dt_FM = 1
    N_content_primary_product_kg_per_dt_FM = 3 * 0.18
    legum_fraction = 1
    EWR_N_fraction_FM = 0.7 * 0.6 # REPRO : TM_EWR*NG_EWR

    std_primary_product_yield_dt_fm_per_ha = 25 / 0.18
    
    SYMB_N_FIX = 0.7
    NS_MAX_E = 50
    NS_MIN_E = 10
    NS_MAX_EWR = 5
    NS_MIN_EWR = 50

    humus_coefficent_stroh = 0
    humus_coefficent_gründung = 0.1 * 0.18
   