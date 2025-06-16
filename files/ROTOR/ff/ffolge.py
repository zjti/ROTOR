from ROTOR.utils.js.jsmodel import  ModelFields as MF
from ROTOR.utils.js.jsmodel import  VisFields as VF
from ROTOR.utils.modelvalue import ModelValue,ClassWithModelValues
from ROTOR.economy.economy import FFEconomy
from ROTOR.utils.weather import monthly_weather_obj, MonthlyWeather

class FFElement( ClassWithModelValues):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pre_crop = None
        self.next_crop = None
        
        pass

    def post_init(self):
        pass

    def serialize(self):
        data= {
            MF.crop : self.crop_data.crop_code,
            'MODELVALUES' : {},
        }

        data['MODELVALUES'] = self.serialize_model_values()
        
        
        #add visible tabs
        tabs = set()
        for model in data['MODELVALUES'].values():
            try:
                tabs.add(model['tab'])
            except:
                pass
        data[MF.vis] = {tab : True for tab in tabs}

        return data
    
    def deserialize(self,data) :
        print(data)
        
        model_values = {value.name : value for value in self.__dict__.values() if isinstance(value, ModelValue)}
        if 'MODELVALUES' in data:
            for modelvalue_name, model_valuedata in data['MODELVALUES'].items():
                
                if 'name_corrected' in model_valuedata:
                    print(model_valuedata[model_valuedata['name_corrected']])
                    print( model_valuedata['name_corrected'])
                    print()
                    if model_valuedata[model_valuedata['name_corrected']] != model_valuedata[model_valuedata['name']]:
                        model_values[modelvalue_name].set_value( model_valuedata[model_valuedata['name_corrected']])
                
        return
        # for key, value in self.user_inputs.items():
            
        #     name_corrected = getattr(self, value).name_corrected
        #     if name_corrected in data:
        #         getattr(self, value).set_value( data[name_corrected] )
    def get_eval_data(self):
        return {'crop':self.crop_data.crop_code, 
                'supplies':self.get_supplies(),
                'removals':self.get_removals()}
        

class FFolge(ClassWithModelValues):
    def __init__(self,length,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.length = length
        self.crops = []
        
        # if not hasattr(self,'ff_economy'):
        self.ff_economy = FFEconomy(ffolge=self, model_value_ref = self )
        
        self.mweather = MonthlyWeather('PRECIPITATION' , model_value_ref = self , model_value_group_name='PRECIPITATION' )
        monthly_weather_obj['PRECIPITATION'] = self.mweather
        
        self.mweather = MonthlyWeather('TEMPERATURE_AVG' , model_value_ref = self , model_value_group_name='TEMPERATURE_AVG' )
        monthly_weather_obj['TEMPERATURE_AVG'] = self.mweather
            
        self.mweather = MonthlyWeather('ET0' , model_value_ref = self , model_value_group_name='ET0' )
        monthly_weather_obj['ET0'] = self.mweather

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
        if ffelement:
                
            ffelement.ff_economy = self.ff_economy
            
        
    def post_init(self):
        for crop in self.crops:
            if crop is not None:
                crop.post_init()
    
    def serialize(self):
        
        ffolge = {}
        for i,crop in enumerate(self.crops):
            if crop is not None:
                ffolge[str(i+1)] = crop.serialize()
            else:
                ffolge[str(i+1)] = {MF.vis :{}}
                
        ffolge['FF_META'] = self.serialize_model_values()
                
        return ffolge
    
    def get_eval_data(self):
        eval_data = []
        for crop in self.crops:
            if crop is None:
                eval_data.append( {} )
            else:
                eval_data.append( crop.get_eval_data() )
        return eval_data
    
 
