def isinstance_by_name(obj, class_name: str, module_prefix: str = None):
    """
    Check if object's class (or any base) matches a given class name,
    optionally within a module prefix (like 'ROTOR.models').
    """
    for cls in obj.__class__.__mro__:
        if cls.__name__ == class_name:
            if module_prefix is None or cls.__module__.startswith(module_prefix):
                return True
    return False