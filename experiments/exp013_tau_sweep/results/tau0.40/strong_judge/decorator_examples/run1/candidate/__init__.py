from functools import wraps

active_registry = set()

def register_function(active=True):
    def decorator(func):
        func.status = "active" if active else "inactive"
        if active:
            active_registry.add(func)
        return func

    if callable(active):  # Check if the first argument is a function
        func = active
        func.status = "active"
        active_registry.add(func)
        return func
    return decorator

def string_conversion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return str(func(*args, **kwargs))
    return wrapper

@register_function
def sample_function_one():
    return None

@register_function(active=False)
def sample_function_two():
    return None

@register_function
def sample_function_three():
    return None
