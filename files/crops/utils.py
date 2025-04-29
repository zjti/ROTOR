import pkgutil
import inspect
from importlib import import_module

from . import crop
from .  import classes

def get_crop_dict(): 

    path = classes.__path__[0]
    crop_dict ={}
    for _,module_name,_ in pkgutil.iter_modules(classes.__path__):
        
        full_module_name = f"crops.classes.{module_name}"
        module = import_module(full_module_name)
        
        # Find all classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                print(obj, issubclass(obj,crop.Crop))
                crop_dict[name] = obj
    return crop_dict
