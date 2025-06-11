import autopep8
import inspect 
import importlib
from glob import glob


def get_class_methods(cls):
    
    funcs = {}
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Determine where the function is defined
        if name in cls.__dict__:
            # print(f"{name}() - defined in {cls.__name__}")
            
            funcs[name] = getattr(cls,name)
        else:
            for base in inspect.getmro(cls)[1:]:  # skip cls itself
                if name in base.__dict__:
                    funcs[name] = getattr(base,name)
                    # print(f"{name}() - inherited from {base.__name__}")
                    break
    return funcs

def get_patched_function_source(cls,method_name):
    class_name = cls.__name__.split('.')[-1]
    filename = f'/drive/ROTOR/utils/user_patches/{class_name}_{method_name}.py'
    print(filename)
    files = glob(filename)
    if len(files) == 0:
        return None

    with open(files[0]) as f:
        src = f.read()
    return src
    
def get_formated_source_for_cls_method(cls, method_name):
    patched_src = get_patched_function_source(cls, method_name)

    method = get_class_methods(cls).get(method_name,None)
    if method:
        src = inspect.getsource(method)
        src=autopep8.fix_code(src)
    return src, patched_src

def get_patched_method(cls, method_name):
    class_name = cls.__name__.split('.')[-1]
    filename = f'/drive/ROTOR/utils/user_patches/{class_name}_{method_name}.py'
    files = glob(filename)
    if len(files) == 0:
        print(f'the patch at {filename} could not be found on disk')
        return None

    try:
        module = importlib.import_module(f'ROTOR.utils.user_patches.{class_name}_{method_name}')
        
        return getattr(module, method_name)
    except Exception as err:
        print(f'the patch at {filename} could not be loaded')
        print('ERROR:', err)
        return None

    