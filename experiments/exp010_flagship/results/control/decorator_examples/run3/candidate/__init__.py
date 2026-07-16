from functools import wraps

active_functions = set()

def register_function(active=True):
    def decorator(func):
        func.status = "active" if active else "inactive"
        if active:
            active_functions.add(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return str(result)  # Convert result to string
        wrapper.status = func.status  # Set status on the wrapper
        return wrapper  # Return the wrapped function
    return decorator