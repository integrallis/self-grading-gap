def register_function(active=True):
    def decorator(func):
        func.status = "active" if active else "inactive"
        if active:
            register_function.registry.append(func)
        return func
    return decorator(func) if callable(active) else decorator

register_function.registry = []


def convert_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result)
    wrapper.__name__ = func.__name__
    wrapper.__dict__.update(func.__dict__)
    return wrapper
