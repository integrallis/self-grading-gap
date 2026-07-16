# file: fibonacci_dynamic.py
from candidate import fibonacci


class Fibonacci:
    def get_number(self, value):
        return fibonacci(value)

    def raises(self, *values):
        return fibonacci(*values)
