# file: decorator_examples.py

from candidate.impl import FunctionRegistry, register_function, add_stringified, subtract_stringified, multiply_stringified

def register(func):
    return register_function(active=True)(func)

def registered(func):
    FunctionRegistry.register(func)
    return func

subject_1 = add_stringified
subject_2 = multiply_stringified
subject_3 = subtract_stringified
