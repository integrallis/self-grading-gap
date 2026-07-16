# file: fibonacci/dynamic.py
from candidate import fibonacci_lookup


class Fibonacci:
    get_number = staticmethod(fibonacci_lookup)
    raises = staticmethod(fibonacci_lookup)
