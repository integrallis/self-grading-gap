# file: decorator_examples.py

from candidate.impl import FunctionRegistry, register_function as register

def registered(func):
    FunctionRegistry.register(func)
    return func

subject_1 = add
subject_2 = subtract
subject_3 = multiply

# Note: The functions add, subtract, and multiply need to be imported here as well.
# However, in the original problem statement, they are not directly exposed.
# To comply strictly, we would assume they are available in the same file or
# their names are explicitly defined as needed.

add = FunctionRegistry.registered_functions[0]
subtract = FunctionRegistry.registered_functions[1]
multiply = FunctionRegistry.registered_functions[2]
