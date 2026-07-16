# candidate/impl.py

class FunctionRegistry:
    registered_functions = []

    @classmethod
    def register(cls, func):
        if getattr(func, 'status', 'inactive') == 'active':
            cls.registered_functions.append(func)
        return func


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
    """Returns the sum of a and b."""
    return a + b


@register_function(active=False)
def subtract(a, b):
    """Returns the difference of a and b."""
    return a - b


@register_function(active=True)
def multiply(a, b):
    """Returns the product of a and b."""
    return a * b


add = stringify_result(add)
subtract = stringify_result(subtract)
multiply = stringify_result(multiply)
