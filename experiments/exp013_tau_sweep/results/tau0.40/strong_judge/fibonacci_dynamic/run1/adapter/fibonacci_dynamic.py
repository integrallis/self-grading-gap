# file: fibonacci_dynamic.py
from candidate import fibonacci as _fibonacci
from candidate import pytest as _pytest


class Fibonacci:
    get_number = staticmethod(_fibonacci)
    raises = staticmethod(_pytest.raises)
