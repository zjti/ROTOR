
from jsmodel import  ModelFields as MF


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
    
    def get_eval_table_hight_detail(self):
        pass
 
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
    