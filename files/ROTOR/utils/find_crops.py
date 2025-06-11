import os
import pkgutil
import inspect
from importlib import import_module

from ROTOR.crop import Crop
from ROTOR  import crops

def get_crop_dict(): 

    path = crops.__path__[0]
    crop_dict ={}
    # print(list(pkgutil.iter_modules(crops.__path__)))
    # print(os.getcwd())
    for _,module_name,_ in pkgutil.iter_modules(crops.__path__):
        
        full_module_name = f"ROTOR.crops.{module_name}"
        module = import_module(full_module_name)
        
        # Find all classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                print(obj, issubclass(obj,Crop),obj,Crop)
                crop_dict[name] = obj
    return crop_dict
