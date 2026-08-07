# file: calculator_tdd_ebook/digit_keys.py
from candidate import DigitGenerator as _DigitGenerator


class DigitKeys(_DigitGenerator):
    other_than = _DigitGenerator.get_digit_except
