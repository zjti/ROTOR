import sys
import importlib

def autoreload(verbose=True):
    print('autoreload')
    f = sorted([(n,mod) for n,mod in sys.modules.items() 
                if hasattr(mod,'__file__') and mod.__file__ is not None and (mod.__file__.startswith('/home') or mod.__file__.startswith('/drive') )],
               key=lambda x:x[1].__file__)
    for n,mod in f:
        if n != 'config': 
            if verbose:
                print(f'reload {mod}')
            sys.modules.pop(n, None)
            # importlib.reload(mod)
            importlib.import_module(n)

    # # print('2. autoreload')
    # f = sorted([(n,mod) for n,mod in sys.modules.items() 
    #             if hasattr(mod,'__file__') and mod.__file__ is not None and (mod.__file__.startswith('/home') or mod.__file__.startswith('/drive') ) ],
    #            key=lambda x:x[1].__file__)
    # for n,mod in f[::-1]:
    #     if n != 'config':
    #         sys.modules.pop(n, None)
    #         importlib.reload(mod)

            
    