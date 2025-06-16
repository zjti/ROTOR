from ROTOR.humus.repro_dyn.repro_base import  ReproHumusMehrer

class LEG_GRAS( ReproHumusMehrer):
    
    std_bilanz_coefficent = 2
    
    pp_bp_ratio = 0
    bp_pp_ratio = 0 #  by_product_yield_dt_fm / primary_product_yield_dt_fm 
    N_content_seed_kg_per_kg = 0.026
    N_content_by_product_kg_per_dt_FM = 1
    N_content_primary_product_kg_per_dt_FM = 2.6 * 0.20
    legum_fraction = 1
    EWR_N_fraction_FM = 0.8 * 0.7 # REPRO : TM_EWR*NG_EWR

    std_primary_product_yield_dt_fm_per_ha = 120 / 0.2
    
    SYMB_N_FIX = 0.9
    NS_MAX_E = 350
    NS_MIN_E = 60
    NS_MAX_EWR = 170
    NS_MIN_EWR = 35

    humus_coefficent_stroh = 0
    humus_coefficent_gründung = 0.1 * 0.2
   