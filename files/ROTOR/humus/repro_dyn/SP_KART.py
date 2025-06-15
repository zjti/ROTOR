from ROTOR.humus.repro_dyn.repro_base import  ReproHumusZehrer

class SP_KART( ReproHumusZehrer):
    
    std_bilanz_coefficent = -2.75
    
    pp_bp_ratio = 0.3
    bp_pp_ratio = 1 / pp_bp_ratio #  by_product_yield_dt_fm / primary_product_yield_dt_fm 
    N_content_seed_kg_per_kg = 0.014
    N_content_by_product_kg_per_dt_FM = 0.9 * 0.4
    N_content_primary_product_kg_per_dt_FM = 1.4 * 0.22
    legum_fraction = 0
    EWR_N_fraction_FM = 0

    humus_coefficent_stroh = 0
    humus_coefficent_gründung = 0.075 * 0.4

    
   