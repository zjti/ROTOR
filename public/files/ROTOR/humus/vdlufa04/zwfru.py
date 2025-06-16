from .vdlufa import VDLUFA

class ZW_UNTER(VDLUFA):
    HP_HÄ_per_ha = 250
    NP_HÄ_per_ha = 0.8
    primary_product_yield_dt_fm_per_ha = 190
    pp_bp_ratio = 1


class ZW_STOPPEL(VDLUFA):
    HP_HÄ_per_ha = 100
    NP_HÄ_per_ha = 0.8
    primary_product_yield_dt_fm_per_ha = 250
    pp_bp_ratio = 1


class ZW_BLANK(VDLUFA):
    HP_HÄ_per_ha = 150
    NP_HÄ_per_ha = 0
    primary_product_yield_dt_fm_per_ha = 250
    pp_bp_ratio = 1

    