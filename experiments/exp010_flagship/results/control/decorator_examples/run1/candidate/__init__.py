from functools import wraps

class RegistrationDecorator:
    def __init__(self):
        self.registered_functions = []

    def register(self, func):
        if getattr(func, 'status', 'inactive') == 'active':
            self.registered_functions.append(func)
        return func

    def convert_to_string(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper():
            return str(func(*args, **kwargs))
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper()

registration_decorator = RegistrationDecorator()

@registration_decorator.register
def active_function():
    """An active function."""
    return None
active_function.status = 'active'

@registration_decorator.register
def another_active_function():
    """Another active function."""
    return None
another_active_function.status = 'active'

@registration_decorator.register
def inactive_function():
    """An inactive function."""
    return None
inactive_function.status = 'inactive'