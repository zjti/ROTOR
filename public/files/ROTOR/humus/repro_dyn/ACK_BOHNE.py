from ROTOR.humus.repro_dyn.repro_base import  ReproHumusMehrer

class ACK_BOHNE( ReproHumusMehrer):
    
    std_bilanz_coefficent = 0.15
    
    pp_bp_ratio = 1.6
    bp_pp_ratio = 1 / pp_bp_ratio #  by_product_yield_dt_fm / primary_product_yield_dt_fm 
    N_content_seed_kg_per_kg = 0.047
    N_content_by_product_kg_per_dt_FM = 1.38 * 0.86
    N_content_primary_product_kg_per_dt_FM = 4.7 * 0.86
    legum_fraction = 1
    EWR_N_fraction_FM = 0.7 * 0.55 # REPRO : TM_EWR*NG_EWR

    std_primary_product_yield_dt_fm_per_ha = 35 / 0.86
    
    SYMB_N_FIX = 0.7
    NS_MAX_E = 210
    NS_MIN_E = 30
    NS_MAX_EWR = 80
    NS_MIN_EWR = 10

    humus_coefficent_stroh = 0.12 * 0.86
    humus_coefficent_gründung = 0
   