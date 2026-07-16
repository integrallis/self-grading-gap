# candidate/impl.py

class FunctionRegistry:
    _registered_functions = []

    @classmethod
    def register(cls, func):
        if getattr(func, 'status', 'inactive') == 'active':
            cls._registered_functions.append(func)
        return func

    @classmethod
    def get_registered_functions(cls):
        return cls._registered_functions


def register_function(active=True):
    def decorator(func):
        func.status = 'active' if active else 'inactive'
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


add_stringified = stringify_result(add)
subtract_stringified = stringify_result(subtract)
multiply_stringified = stringify_result(multiply)
