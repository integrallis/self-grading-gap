# candidate/impl.py

from functools import wraps
from decorator_examples import register, registered, subject_1, subject_2, subject_3

# Shared collection for active functions
active_functions = []

def register_function(active=True):
    """
    A decorator to register functions based on their activation status.
    """
    def decorator(func):
        # Set the activation status
        func.status = "active" if active else "inactive"
        
        # Add to active functions registry if active
        active_functions.append(func) if active else None

        # Return the unchanged function
        return func
    
    return decorator

def stringify_result(func):
    """
    A decorator to convert the return value of a function to its string form.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result)  # Convert the result to string

    return wrapper

@register_function(active=True)
@stringify_result
def add(a, b):
    """
    Adds two numbers.
    """
    return a + b

@register_function(active=False)
def subtract(a, b):
    """
    Subtracts the second number from the first.
    """
    return a - b

@register_function(active=True)
@stringify_result
def multiply(a, b):
    """
    Multiplies two numbers.
    """
    return a * b
