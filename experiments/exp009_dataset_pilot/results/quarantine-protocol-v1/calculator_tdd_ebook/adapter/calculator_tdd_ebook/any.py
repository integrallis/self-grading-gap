# file: calculator_tdd_ebook/any.py

from candidate.impl import DigitGenerator as _DigitGenerator

class Any:
    def __init__(self):
        self._generator = _DigitGenerator()

    def other_than(self, excluded_digit):
        return self._generator.any_other_than(excluded_digit)
