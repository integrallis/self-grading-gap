# file: fibonacci_brute_force.py
from candidate import fibonacci, pytest


class Fibonacci:
    get_number = staticmethod(fibonacci)
    raises = staticmethod(pytest.raises)
