from ROTOR.humus.repro_dyn.repro_base import  ReproHumusZehrer

class WN_GERSTE( ReproHumusZehrer):
    
    std_bilanz_coefficent = -1.05
    
    pp_bp_ratio = 1.2
    bp_pp_ratio = 1 / pp_bp_ratio #  by_product_yield_dt_fm / primary_product_yield_dt_fm 
    N_content_seed_kg_per_kg = 0.017
    N_content_by_product_kg_per_dt_FM = 0.45 * 0.86
    N_content_primary_product_kg_per_dt_FM = 1.7 * 0.86
    legum_fraction = 0
    EWR_N_fraction_FM = 0

    humus_coefficent_stroh = 0.14 * 0.86
    humus_coefficent_gründung = 0
   