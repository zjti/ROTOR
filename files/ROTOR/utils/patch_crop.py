import os
import types
from ROTOR.utils.load_patch import get_patched_method 
from ROTOR.utils.user_input import UserEditableModelValue
from ROTOR.utils.find_crops import get_crop_dict
from glob import glob

def patch_crop_dict():
    crop_dict = get_crop_dict()
    for v in crop_dict.values():
        patch_crop(v)
        
def patch_crop( C ):
    base_cls_name = C.__name__

    def patch_helper( method, patch_method):
        def f(self,  *args,**kwargs):
            try:
                return patch_method(self, *args,**kwargs)
            except Exception as e:
                print('fallback ', e)
                return method(self, *args,**kwargs)
        return f
    
    
    patchfiles = glob(f'ROTOR/utils/user_patches/{base_cls_name}_*')
    for patch in patchfiles:
        method_name = os.path.basename(patch)[len(base_cls_name)+1:-3]
        patch_method = get_patched_method(base_cls_name, method_name)
    
        if hasattr(C, method_name):
            user_can_overwrite = False
            user_can_overwrite_arg = None
            if hasattr(getattr(C,method_name), 'user_can_overwrite_arg') :
                user_can_overwrite_arg = getattr(C,method_name).user_can_overwrite_arg
                user_can_overwrite = True
            
            if hasattr(patch_method, 'user_can_overwrite_arg') :
                user_can_overwrite_arg = patch_method.user_can_overwrite_arg
                user_can_overwrite = True
            
           
            func_wrapper = patch_helper(getattr(C,method_name) , patch_method)
            
            
            if user_can_overwrite:
                func_wrapper.user_can_overwrite = True
                func_wrapper.user_can_overwrite_arg = user_can_overwrite_arg
            
            setattr(C, method_name, func_wrapper)
    
    
  
                
    cls = C
    user_can_overwrite_methods = {
        name: (getattr(C, name).user_can_overwrite_arg if hasattr(getattr(C, name), "user_can_overwrite_arg") else None)
        for cls in C.__mro__  # Look through all base classes
        for name in dir(cls)
        if callable(getattr(cls, name)) and hasattr(getattr(cls, name), "user_can_overwrite")
    }

    # user_inputs = {}
    # for user_can_overwrite_method in user_can_overwrite_methods.keys():
        
    #     user_can_overwrite_arg = None
    #     for cls in C.__mro__:
    
    #         for name in dir(cls):
    #             if hasattr(getattr(cls, name), "user_can_overwrite_arg"):
    #                 user_can_overwrite_arg = getattr(getattr(cls, name), "user_can_overwrite_arg")
         
    #     get_value, get_model = UserEditableModelValue(  getattr(C, user_can_overwrite_method), user_can_overwrite_method )
    #     setattr(C, user_can_overwrite_method , get_value)
    #     setattr(C, user_can_overwrite_method + '__get_model' , get_model)
    
    #     get_value.user_can_overwrite = True
    #     get_value.user_can_overwrite_arg = user_can_overwrite_arg

    #     user_inputs[ 'func' ] = user_can_overwrite_method
    #     user_inputs[ 'name_corrected' ] = user_can_overwrite_method
        
    # C.user_inputs = user_inputs
    
    return C