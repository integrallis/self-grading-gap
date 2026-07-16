# file: fibonacci_brute_force.py
from candidate import fibonacci as _fibonacci


class Fibonacci:
    def get_number(self, argument):
        return _fibonacci(argument)

    def raises(self, *arguments):
        return _fibonacci(*arguments)
