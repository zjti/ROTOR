from dataclasses import dataclass
from typing import Optional, Dict, Type
from .cropdata import HarvestProduct,CropData
from . import cropdata 
import config

from .cropopts import CropOpts as CO
from jsmodel import  ModelFields as MF
from jsmodel import  VisFields as VF

import fertilizer


class FFElement:
    def __init__(self):
        self.pre_crop = None
        self.next_crop = None
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
            if crop is not None:
                ffolge[str(i+1)] = crop.serialize()
            else:
                ffolge[str(i+1)] = {MF.vis :{}}
                
        return ffolge
    
    def get_eval_data(self):
        eval_data = []
        for crop in self.crops:
            if crop is None:
                eval_data.append( {} )
            else:
                eval_data.append( crop.get_eval_data() )
        return eval_data
        
class ModelValue:
    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value
    
    def get_model(self):
        return {self.name : self.default_value() }
        
    def get_value(self):
        return self.default_value()

class UserEditableModelValue(ModelValue):
    def __init__(self, name, default_value = None ,
                 name_corrected = None , user_value = None):
        self.user_value = user_value
        if name_corrected:
            self.name_corrected = name_corrected
        else:
            self.name_corrected = name + '_corrected'
        super().__init__(name,default_value)
    
    def user_modified(self):
        return self.user_value != self.default_value()
    
    def get_model(self):
        return {self.name : self.default_value(),
                self.name_corrected : self.get_value()}
    
    def parse_from_dict(self, data):
        if self.name in data:
            self.default_value = data[self.name]
        if self.name_corrected in data:
            self.user_value = data[self.name_corrected]
           
    def get_value(self):
        if self.user_value:
            return  self.user_value
        return self.default_value()              
    
class Crop(FFElement):
    def __init__(self, crop_data: CropData):
        super().__init__()

        self.crop_data = crop_data
        
        self.crop_specific_leaching_coefficent = 0.1
        self.has_covercrop = False
        
        self.fertilizer_applications = fertilizer.FertilizerApplications()

        self.seeds_kg_per_ha = UserEditableModelValue(
            name=MF.seeds_kg_per_ha, 
            default_value  = lambda : self._seeds_kg_per_ha,
            name_corrected=MF.seeds_kg_per_ha_corrected)
        
        self._seeds_kg_per_ha = 100
        
    
    def get_supplies(self):
        supplies = []
        N = self.seeds_kg_per_ha.get_value() /100 * self.get_primary_product_nitrogen_kg_per_dt()
        P = self.seeds_kg_per_ha.get_value() /100 * self.crop_data.primary_product.phosphate_oxide_kg_per_dt * 0.4364
        K = self.seeds_kg_per_ha.get_value() /100 * self.crop_data.primary_product.potassium_oxide_kg_per_dt * 0.83 
        
        supplies.append( {MF.supply_name : MF.seed_supply, 'N':N, 'P':P, 'K':K , MF.supply_info: ""})
            
        return supplies
    
    def get_N_uptake(self):
        return -1
    
    def calc_N_leaching_kg_per_ha(self):
        N_manure_p= self.fertilizer_applications.get_N_avail_from_fert_kg_per_ha()
        
        N_mineralization = (config.SOIL['MIN_RATE_OBS']['default'] * 0.01 *
                            config.SOIL['C_N_QUOT']['default'] * 0.01 *
                            config.SOIL['ORG_SUBS']['default'] * 0.01 *
                            config.SOIL['ROHDICHTE_TOPSOIL']['default']  *
                            config.SOIL['OBERBODEN']['default'] *
                            (100 - config.SOIL['PARTICLE_GEQ_2MM']['default']) * 0.01 *
                            100000 )
        
        N_dfs = self.get_N_uptake() - config.SOIL['N_DEPO']['default']
        
        N_surplus = N_manure_p + N_mineralization - N_dfs
        
        N_leaching_prob = config.SOIL['WINTER_NIEDERSCHLAG']['default']  / config.SOIL['FELD_KAPA']['default']
        
        
        N_leaching = N_surplus * N_leaching_prob
        N_leaching *= self.crop_specific_leaching_coefficent
        return N_leaching, f"leachingprob {N_leaching_prob:.2f}  surpl{N_surplus:.2f} {N_mineralization:.2f}"
    
    def get_removals(self):
        removals = []
        # //n_leaching_removal
        N,ninfo = self.calc_N_leaching_kg_per_ha()
        
        removals.append( {MF.removal_name : MF.n_leaching_removal, 'N':N, MF.removal_info: ninfo})

        return removals
    
    def serialize(self):
        data= {
            MF.crop : self.crop_data.crop_code,
            MF.vis : {VF.anbau_tab : True },
        }
        data.update(self.seeds_kg_per_ha.get_model())
        return data
    
    def deserialize(self,data) :
        
        if self.seeds_kg_per_ha.name_corrected in data:
            self.seeds_kg_per_ha.user_value = data[self.seeds_kg_per_ha.name_corrected]
            
    
    def get_eval_data(self):
        data = {
            
            MF.crop : self.crop_data.crop_code,
        }
        data.update( self.seeds_kg_per_ha() )

        return data

class CropWithYield(Crop):
    def __init__(self, crop_data: CropData):
        super().__init__(crop_data = crop_data)
 
        self.yield_dt = UserEditableModelValue(
            name=MF.yield_dt_calc, 
            default_value  = lambda : self.calc_yield_dt(),
            name_corrected=MF.yield_dt_corrected)
        
        self.byproduct_yield_dt = UserEditableModelValue(
            name=MF.nebenprodukt_yield_dt_calc ,
            default_value  = lambda : self.calc_byproduct_yield_dt(),
            name_corrected=MF.nebenprodukt_yield_dt_corrected)
        
        self.primary_product_crude_protein_percent = UserEditableModelValue(
            name = MF.crude_protein_content,
            default_value= lambda : crop_data.primary_product.crude_protein_percent,
            name_corrected= MF.crude_protein_content_corrected )
        
        self.yield_from_fert_dt = ModelValue(
            name = MF.yield_from_fert_dt,
            default_value= lambda : self.calc_yield_from_fert_dt()
        )
        

    def get_crop_opts():
        return []

    def can_covercrop(self):
        return False
    
    def calc_yield_dt(self):    
        return 0
    
    def calc_byproduct_yield_dt(self):
        return 0
    
    def calc_yield_from_fert_dt(self):
        return 0
    
    def serialize(self):
        data = super().serialize()
        
        data[MF.vis].update(self.get_vis())
        
        data.update( self.yield_dt.get_model() )
        data.update( self.byproduct_yield_dt.get_model() )
        data.update( self.primary_product_crude_protein_percent.get_model() )
        data.update( self.yield_from_fert_dt.get_model() )
        
        data[MF.evaluation ] = {}
        data[MF.evaluation ][ MF.removals ] = self.get_removals()
        data[MF.evaluation ][ MF.supplies ] = self.get_supplies()
         
        return data

    def deserialize(self,data) :
        super().deserialize(data)
        
        for user_editable_model_values in [
            self.yield_dt,
            self.byproduct_yield_dt,
            self.primary_product_crude_protein_percent
        ]:    
            if user_editable_model_values.name_corrected in data:
                user_editable_model_values.user_value = data[user_editable_model_values.name_corrected]
            
    def get_supplies(self):
        supplies = super().get_supplies()
        if not self.fertilizer_applications.isEmpty():
            N,P,K = self.fertilizer_applications.get_NPK_from_fert_kg_per_ha()
            menge = self.fertilizer_applications.get_amount_t_per_ha()
            supplies.append( {MF.supply_name: MF.fertilizer_supply,  'N':N, 'P':P, 'K':K , MF.supply_info: f"{menge} t/ha" } )
            
        return supplies
        
    def get_removals(self):
        removals = super().get_removals()
        N = self.yield_dt.get_value() * self.get_primary_product_nitrogen_kg_per_dt()
        P = self.yield_dt.get_value() * self.crop_data.primary_product.phosphate_oxide_kg_per_dt * 0.4364
        K = self.yield_dt.get_value() * self.crop_data.primary_product.potassium_oxide_kg_per_dt * 0.83 
        removals.append( {MF.removal_name : MF.primary_harvest_removal, 'N':N, 'P':P, 'K':K , MF.removal_info: "-"})
        return removals

    def get_primary_product_nitrogen_kg_per_dt(self):

        if self.primary_product_crude_protein_percent.user_modified():
            return self.primary_product_crude_protein_percent.get_value() / 5.7
    
        return self.crop_data.primary_product.nitrogen_kg_per_dt  
    
    
    def get_eval_data(self):
        data = {
            MF.crop : self.crop_data.crop_code,
            MF.removals : self.get_removals(),
            MF.supplies : self.get_supplies()
        }
        
        return data
    
    
    def get_N_uptake(self):
        N = self.byproduct_yield_dt.get_value() * self.crop_data.straw_product.nitrogen_kg_per_dt
        N+= self.yield_dt.get_value() * self.crop_data.primary_product.nitrogen_kg_per_dt
        return N
        
    def calc_yield_from_fert_dt(self):
        N_from_fert = self.fertilizer_applications.get_N_avail_from_fert_kg_per_ha()
        return  N_from_fert  / self.get_primary_product_nitrogen_kg_per_dt() 
        

    def get_vis(self):
        return {VF.ertrag_tab :True}
     
    def calc_N_fixation_kg_per_ha(self) -> float:
        return 0.0  # normal crops don't fix nitrogen
    
    
    
class CropWithByProductHarvest(CropWithYield ):
    """Cereal crop group"""
    GROUP_NAME = "Getreide"
    
    def __init__(self, crop_data):
        super().__init__(crop_data)
        self.byproduct_harvest = True
    
    def deserialize(self, data):
        if MF.dung_menge in data:
            self.fertilizer_applications.deserialize(data[MF.dung_menge])
        if MF.stroh in data :
            self.byproduct_harvest = data[MF.stroh]
        return super().deserialize(data)
    
    def serialize(self):
        data = super().serialize()
        data[MF.vis][VF.dung_tab] = True 
        data[MF.vis][VF.anbau_tab] = True 
        data[MF.vis][VF.stroh_opt] = True 
        data[MF.stroh] = self.byproduct_harvest
        
        data[MF.dung_menge] = self.fertilizer_applications.dung_menge
        return data
    
    def get_removals(self):
        removals = super().get_removals()
        
        if self.byproduct_harvest:
            N = self.byproduct_yield_dt.get_value() * self.crop_data.straw_product.nitrogen_kg_per_dt
            P = self.byproduct_yield_dt.get_value() * self.crop_data.straw_product.phosphate_oxide_kg_per_dt * 0.4364
            K = self.byproduct_yield_dt.get_value() * self.crop_data.straw_product.potassium_oxide_kg_per_dt * 0.83 
            removals.append( {MF.removal_name : MF.byproduct_harvest_removal, 'N':N, 'P':P, 'K':K , MF.removal_info: "-"})
        return removals
    
    
    
class CropWithCoverCrop(CropWithYield):
    
    def __init__(self, crop_data):
        super().__init__(crop_data)
        
        self.covercrop_yield_dt = UserEditableModelValue(
            name=MF.covercrop_yield_dt,
            default_value  = lambda : self.calc_covercrop_yield_dt(),
            name_corrected=MF.covercrop_yield_dt_corrected)
        
        self.zw_plant = "Blanksaat"
        self.zwischenfrucht_winterhard = 'abfrierend'
        self.zwischenfrucht_schnittnutz = 'Einarbeitung'
        self.zwischenfrucht_legant = 23
        
    def calc_covercrop_yield_dt(self):
        return 5.4
    
    def get_zw_plant_opts(self):
        opts = ["Blanksaat","Stoppelsaat"]
        if self.pre_crop:
            if CO.CAN_UNDERSAWN_AFTER in self.pre_crop.get_crop_opts():
                opts += ['Untersaat']
        return opts
        
    def can_covercrop(self):
        if self.pre_crop:
            if CO.CAN_COVERCROP_AFTER not in self.pre_crop.get_crop_opts():
                return False
        return True
    
    def deserialize(self, data):
         
        if MF.zw in data :
            self.has_covercrop = data[MF.zw]
            if not self.can_covercrop() :
                self.has_covercrop = False
        if self.has_covercrop:
            if MF.zw_plant in data:
                self.zw_plant = data[MF.zw_plant]
            if MF.zwischenfrucht_winterhard in data:
                self.zwischenfrucht_winterhard = data[MF.zwischenfrucht_winterhard]
            if MF.zwischenfrucht_legant in data:
                self.zwischenfrucht_legant = data[MF.zwischenfrucht_legant]
            if MF.zwischenfrucht_schnittnutz in data:
                self.zwischenfrucht_schnittnutz = data[MF.zwischenfrucht_schnittnutz] 
            
        if self.covercrop_yield_dt.name_corrected in data:
            self.covercrop_yield_dt.user_value = data[self.covercrop_yield_dt.name_corrected]
            
            
        return super().deserialize(data)
    
    def serialize(self):
        data = super().serialize()
        data[MF.vis][VF.has_herbst_gabe] = False
        if self.can_covercrop():
            data[MF.vis][VF.zw_opt] = True
            data[MF.zw] = self.has_covercrop
        if self.has_covercrop:
            data[MF.zwischenfrucht_legant] = 13
            data[MF.zw_plant] = self.zw_plant
            data[MF.zw_plant_opts] = self.get_zw_plant_opts()
            data[MF.zwischenfrucht_legant] = self.zwischenfrucht_legant
            data[MF.zwischenfrucht_winterhard] = self.zwischenfrucht_winterhard
            data[MF.zwischenfrucht_schnittnutz] = self.zwischenfrucht_schnittnutz
            
        data.update( self.covercrop_yield_dt.get_model() )
            
        return data
    
class WinterGetreide(CropWithByProductHarvest):
    """Winter-Cereal crop group"""
    GROUP_NAME = "WinterGetreide" 
    
    def serialize(self):
        data = super().serialize()
        data[MF.vis][VF.has_herbst_gabe] = True
        return data
    

class SommerGetreide(CropWithByProductHarvest, CropWithCoverCrop):
    """Sommer-Cereal crop group"""
    GROUP_NAME = "SommerGetreide"
     

class Leguminosen(CropWithYield):
    """Legume crop group """
    GROUP_NAME = "Leguminosen"
    
    def calc_N_fixation_kg_per_ha(self) -> float:
        return self.crop_data.n_fix_kg_per_dt * self.yield_dt.get_value()
    
    def get_supplies(self):
        supplies = super().get_supplies()
        
        N = self.calc_N_fixation_kg_per_ha()
        supplies.append( {MF.supply_name: MF.fixation_supply,  'N':N , MF.supply_info: "" } )
        
        return supplies
    
     
class Hackfrüchte(CropWithYield):
    """Root crop group"""
    GROUP_NAME = "Hackfrüchte"
    
    
    