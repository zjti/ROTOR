from dataclasses import dataclass
from typing import Optional, Dict, Type
from .cropdata import HarvestProduct,CropData
from . import cropdata 
import config


class FFElement:
    def __init__(self):
        pass
        

class FFolge:
    def __init__(self,length):
        self.length = length
        self.crops = []

    def add_crop(self,ffelement):
        self.crops.append(ffelement)
        if len(self.crops) > 1:
            if self.crops[-2]:
                self.crops[-2].next_crop = self.crops[-1]
            if self.crops[-1]:
                self.crops[-1].pre_crop = self.crops[-2]
          
        if self.length == len(self.crops):
            if self.crops[-1]:
                self.crops[-1].next_crop = self.crops[0]
            if self.crops[0]:
                self.crops[0].pre_crop = self.crops[-1]
            
    def serialize(self):
        
        ffolge = {}
        for i,crop in enumerate(self.crops):
            if crop:
                ffolge[str(i+1)] = crop.serialize()
            else:
                ffolge[str(i+1)] = {}
                
        return ffolge
        

class Crop(FFElement):
    """Base crop class with common functionality"""
    def __init__(self, crop_data: CropData):
        self.crop_data = crop_data
        
        super().__init__()

    def serialize(self):
        data= {}
        data['crop'] = self.crop_data.crop_code
        data['vis'] = {'ertrag_tab':True}
        data['yield_dt_corrected'] = 12.34
        data['crude_protein_content_corrected'] = self.crop_data.primary_product.crude_protein_percent
        return data

    def get_N_from_fert(self):
        ffcomp = config.FFolge[self.jahr_key]
        N=0
        
        if  'dung_menge' not in ffcomp:
            return N
 
        # {'fest frisch rind': {'menge': 4, 'is_herbst': False}}...
        for dung_key,dung_val in ffcomp['dung_menge'].items():
            dung_param = config.DUNG_DATA[dung_key]

            N += dung_val['menge'] * dung_param['N/FM'] * ( 100 - dung_param['Nloss'] ) / 100
            #Navil_spring': 20, 'Navil_autumn': 20
            if dung_val['is_herbst']:
                N *= dung_param['Navil_autumn'] / 100
            if dung_val['is_herbst']:
                N *= dung_param['Navil_spring'] / 100
            
        return N
    
    def get_primary_product_nitrogen_kg_per_dt(self):
        ffcomp = config.FFolge[self.jahr_key]
        
        if 'raw_protein_content_corrected' in ffcomp:
            if ffcomp['raw_protein_content_corrected'] != ffcomp['raw_protein_content']:
                return ffcomp['raw_protein_content_corrected'] / 5.7
        
        return self.crop_data.primary_product.nitrogen_kg_per_dt  

    def calc_yield_from_fert_dt(self):
        N_from_fert = self.get_N_from_fert()
        if N_from_fert == 0:
            # print('N_from_fert', N_from_fert)
            return 0.0
        # print('xxb',N_from_fert, self.crop_data.primary_product.nitrogen_kg_per_dt)
        # print(N_from_fert    / self.crop_data.primary_product.nitrogen_kg_per_dt)
        return  N_from_fert    / self.get_primary_product_nitrogen_kg_per_dt() 
    
    def get_models(self):
            
        ffcomp = config.FFolge[self.jahr_key]
        
        yield_from_fert_dt = self.calc_yield_from_fert_dt()
        yield_dt = self.calc_yield_dt_fm_per_ha()  + yield_from_fert_dt

        by_product_yield_dt = yield_dt * self.crop_data.hnv_ratio
        
        always_remove =[ ]
        always_update  = ['yield_dt_calc','yield_from_fert_dt','raw_protein_content',
                          'nebenprodukt_yield_dt_calc' ]
        
        if 'yield_dt_calc' in ffcomp:
            if ffcomp['yield_dt_calc'] == ffcomp['yield_dt_corrected']:
                always_update += ['yield_dt_corrected']
        
        if 'raw_protein_content' in ffcomp:
            if ffcomp['raw_protein_content'] == ffcomp['raw_protein_content_corrected']:
                always_update += ['raw_protein_content_corrected']

        if 'nebenprodukt_yield_dt_calc' in ffcomp:
            if ffcomp['nebenprodukt_yield_dt_calc'] == ffcomp['nebenprodukt_yield_dt_corrected']:
                always_update += ['nebenprodukt_yield_dt_corrected']

        roundoff = lambda x:  float(int(x *100 ) / 100) if x != 0 else 0

        has_herbst_gabe = 'HAS_HERBST' in self.get_crop_opts()

        models = {'has_herbst_gabe':has_herbst_gabe, 'dung_menge':{} , 
                'yield_dt_calc': roundoff( yield_dt ), 
                'yield_dt_corrected': roundoff( yield_dt ),
                'yield_from_fert_dt':roundoff( yield_from_fert_dt),
                'nebenprodukt_yield_dt_calc' : roundoff( by_product_yield_dt),
                'nebenprodukt_yield_dt_corrected' : roundoff( by_product_yield_dt),
                'raw_protein_content': roundoff( self.crop_data.primary_product.crude_protein_percent),
                'raw_protein_content_corrected': roundoff( self.crop_data.primary_product.crude_protein_percent )
                }
        
        ## add byproductharvest
        if 'STROH' in self.get_crop_opts():
            models['stroh'] = True

        ## add catchcrop / zwischenfrucht 
        pre_crop_key = int(self.jahr_key) - 1
        if pre_crop_key == 0:
            pre_crop_key = len(config.FFolge)
        pre_crop_key = str(pre_crop_key)
        ffcomp_pre = config.FFolge[pre_crop_key]

        # is undersawing (catchcrop an option) ?
        us_opt = True 
            
        if pre_crop_key in config.py_FFolge:
            if 'US_NACH' not in config.py_FFolge[pre_crop_key].get_crop_opts():
                us_opt = False 
         

        zw_opt = True
        if 'ZW_VOR' not in self.get_crop_opts():
            zw_opt = False

        if pre_crop_key in config.py_FFolge:
            if 'ZW_NACH' not in config.py_FFolge[pre_crop_key].get_crop_opts():
                zw_opt = False
        
        if zw_opt:
            models ['zw'] = False
            models['zw_plant_opts'] = ['Blanksaat','Stoppelsaat']
            if us_opt :
                models['zw_plant_opts'] += ['Untersaat']
                
            models['zw_plant'] = 'Blanksaat'
            models['zwischenfrucht_legant'] = 13
            models['zwischenfrucht_winterhard'] = 'frosthart'
            models['zwischenfrucht_schnittnutz'] = 'Einarbeitung'

            always_update+= ['zw_plant_opts']
            
            if us_opt == False and 'zw_plant' in ffcomp and ffcomp['zw_plant'] == 'Untersaat':
                models['zw_plant'] = 'Blanksaat'
                always_update+= ['zw_plant']
        else:
            always_remove +=[ 'zw','zw_plant' ,'zwischenfrucht_schnittnutz','zwischenfrucht_winterhard',
                             'zw_plant_opts' ]
        return models , always_update, always_remove
               
        

    def get_vis(self):
        return {'ertrag_tab':True}
    
    def get_crop_opts(self):
        return []
    
class Getreide(Crop):
    """Cereal crop group"""
    GROUP_NAME = "Getreide"
    
    def calc_n_fixation(self) -> float:
        return 0.0  # Cereals don't fix nitrogen

class SommerGetreide(Getreide):
    """Sommer-Cereal crop group"""
    GROUP_NAME = "SommerGetreide"
    
    def calc_n_fixation(self) -> float:
        return 0.0  # Cereals don't fix nitrogen

class WinterGetreide(Getreide):
    """Winter-Cereal crop group"""
    GROUP_NAME = "WinterGetreide"
    
    def calc_n_fixation(self) -> float:
        return 0.0  # Cereals don't fix nitrogen

     

class Leguminosen(Crop):
    """Legume crop group"""
    GROUP_NAME = "Leguminosen"
    
    def calc_n_fixation(self) -> float:
        return self.crop_data.n_fix_kg_per_dt * self.calc_yield_dt_fm_per_ha
    
    def calc_p_balance(self, area_ha: float, p_input: float) -> float:
        removal = self.crop_data.phosphate_kg_per_dt * self.calc_yield(area_ha)
        return p_input - removal

class Hackfrüchte(Crop):
    """Root crop group"""
    GROUP_NAME = "Hackfrüchte"
    
    def calc_n_fixation(self, area_ha: float) -> float:
        return 0.0  # Root crops don't fix nitrogen
