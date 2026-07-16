# file: fibonacci/dynamic.py
from candidate import fibonacci_lookup, pytest


class Fibonacci:
    def get_number(self, *args, **kwargs):
        return fibonacci_lookup(*args, **kwargs)

    def raises(self, *args, **kwargs):
        return pytest.raises(*args, **kwargs)
