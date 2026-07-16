# candidate/impl.py

class FunctionRegistry:
    registered_functions = []

    @staticmethod
    def register(func):
        if getattr(func, 'active', False):
            FunctionRegistry.registered_functions.append(func)
        return func

def register_function(active=True):
    def decorator(func):
        func.active = 'active' if active else 'inactive'
        FunctionRegistry.register(func)
        return func
    return decorator

def stringify_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

@register_function(active=True)
def add(a, b):
    """Add two numbers."""
    return a + b

@register_function(active=False)
def subtract(a, b):
    """Subtract two numbers."""
    return a - b

@register_function(active=True)
def multiply(a, b):
    """Multiply two numbers."""
    return a * b

# Apply stringification to the arithmetic functions
add = stringify_result(add)
subtract = stringify_result(subtract)
multiply = stringify_result(multiply)
