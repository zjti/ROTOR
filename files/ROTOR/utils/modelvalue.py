from ROTOR.utils.isinstance_by_name import isinstance_by_name 

class ClassWithModelValues:
    def __init__(self,  model_values=None, model_value_ref=None , model_value_group_name=None ):
        self._model_values = model_values
        self._model_value_group_name = model_value_group_name
        if model_value_ref:
            if hasattr(model_value_ref,'_model_values') and model_value_ref._model_values is not None :
                if self._model_value_group_name is None:
                    self._model_values = model_value_ref._model_values 
                else:
                    if self._model_value_group_name  in model_value_ref._model_values:
                        self._model_values = model_value_ref._model_values[self._model_value_group_name] 
                    
            self._model_value_ref = model_value_ref

            # add link from parent to child [ in case this objact (aka self) is not assigned to model_value_ref ]
            setattr(model_value_ref, '_model_child_'+str(id(self)), self)
             
    def serialize_model_values(self):
        # print(' serialize_model_values(self)',self)
        model_values = {} 
        # model_data = {value : value.get_model() for name, value in self.__dict__.items() if isinstance(value, ModelValue)}
        model_data = {self.__dict__[name] : self.__dict__[name].get_model() for name in list(self.__dict__.keys()) 
                      if isinstance_by_name(self.__dict__[name], "ModelValue")}
        # print(' len(model_data)', len(model_data))
        for value, model in model_data.items():
            model_values[value.name] = model 

        for name in list(self.__dict__.keys()):
            value = self.__dict__[name]
        
            # if isinstance(value, ClassWithModelValues) :
            # print(name,value)
            if isinstance_by_name(value, 'ClassWithModelValues') :
            
                if hasattr(value, '_model_value_ref'):
                    if value._model_value_ref == self:
                        model_values.update(value.serialize_model_values())

        if self._model_value_group_name is None:
            return model_values
        else:
            return {self._model_value_group_name : model_values }

class ModelValue:
    def __init__(self, name, default_value=None, tab='', type='', unit='', visible=True, select_opts=None):
        self.name = name
        self.default_value = default_value
        self.tab = tab
        self.type = type
        self.unit = unit
        self.visible = visible
        self.select_opts=select_opts

        
        bound_method = default_value
        
        self.instance = bound_method.__self__
        
        for attr in dir(self.instance):
            if getattr(self.instance, attr) == bound_method:
                method_name = attr
                # print(method_name,attr)
                break
        self.method_name = method_name    
        self.bound_method = bound_method
        setattr(self.instance, method_name, self )
        setattr(self.instance, method_name + "__org_func" , bound_method)
        
    def get_model(self):
        model = {'name': self.name,
               'tab': self.tab,
               'type': self.type,
               'visible': self.visible}
        if callable(self.default_value):
            value = self.default_value() 
        else:
            value = self.default_value

        if isinstance(value, float):
            value = round(value, 2)
        model[self.name] = value
        
        if self.unit:
            model['unit'] = self.unit
            
        return model
                
    def get_value(self):
        return self.default_value()



    def __call__(self,*args,**kwargs):
        return self.get_value(*args,**kwargs)
        

class UserEditableModelValue(ModelValue):
    def __init__(self, name, 
                 default_value = None ,
                 name_corrected = None , 
                 user_value = None,
                 **kwargs):
        
        super().__init__(name,default_value,**kwargs)
        
        self.user_value = user_value
        if name_corrected:
            self.name_corrected = name_corrected
        else:
            self.name_corrected = name + '_corrected'
 
        if hasattr(self.instance,'_model_values') and self.instance._model_values and name in self.instance._model_values: 
            stored_model = self.instance._model_values[name]            
            if stored_model[stored_model['name_corrected']] != stored_model[stored_model['name']]:
                self.user_value = stored_model[ stored_model['name_corrected' ]]
                

         
    
    def user_modified(self):
        return self.user_value != self.default_value()
    
    def get_model(self):
        model = super().get_model()

        if self.type == 'select' and self.select_opts:
            if callable(self.select_opts):
                model['select_opts'] = self.select_opts()
            else:
                model['select_opts'] = self.select_opts

        value = self.get_value()
        if isinstance(value, float):
            value = round(value, 2)
        model.update( {  'name_corrected': self.name_corrected, 
                self.name_corrected : value} )
        
        return model
           
    def get_value(self): 
        if self.user_value is not None:
            
            if self.type == 'select' and self.select_opts:
                #check if user value is in opts:
                if callable(self.select_opts):
                    opts = self.select_opts()
                else:
                    opts = self.select_opts
                if self.user_value not in opts:
                    self.user_value = self.default_value()
                
            return  self.user_value
        return self.default_value() 

    def set_value(self,value):
        self.user_value = value