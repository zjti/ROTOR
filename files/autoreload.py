import sys
import importlib

def autoreload(filename):
    print('autoreload')
    f = sorted([(n,mod) for n,mod in sys.modules.items() 
                if hasattr(mod,'__file__') and mod.__file__.startswith('/home') ],
               key=lambda x:x[1].__file__)
    for n,mod in f[::-1]:
        if n != 'config': 
            importlib.reload(mod)

    print('2. autoreload')
    f = sorted([(n,mod) for n,mod in sys.modules.items() 
                if hasattr(mod,'__file__') and mod.__file__.startswith('/home') ],
               key=lambda x:x[1].__file__)
    for n,mod in f[::-1]:
        if n != 'config': 
            importlib.reload(mod)

    