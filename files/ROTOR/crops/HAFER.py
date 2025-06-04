
from ROTOR.cerial import SummerCerial
from ROTOR.crops.data import cropdata


class HAFER(SummerCerial): 
    def __init__(self,*args,**kwargs):
        super().__init__(crop_data = cropdata.HAFER, *args, **kwargs)
        
        
         
    def calc_yield_dt_fm_per_ha(self,EF=2):
        return 12.34