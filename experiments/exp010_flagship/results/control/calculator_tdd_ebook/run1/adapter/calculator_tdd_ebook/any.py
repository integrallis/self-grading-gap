# file: calculator_tdd_ebook/any.py
from candidate import pytest as _pytest


class Any:
    raises = staticmethod(_pytest.raises)
