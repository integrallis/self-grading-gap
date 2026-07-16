# file: fibonacci/dynamic.py
from candidate import fibonacci_lookup as _fibonacci_lookup


class Fibonacci:
    get_number = staticmethod(_fibonacci_lookup)
    raises = staticmethod(_fibonacci_lookup)
