from ROTOR.utils.modelvalue import ClassWithModelValues

class Economy( ClassWithModelValues ):

    def __init__(self, ffelement=None, *args,**kwargs):
        super().__init__(*args,**kwargs)