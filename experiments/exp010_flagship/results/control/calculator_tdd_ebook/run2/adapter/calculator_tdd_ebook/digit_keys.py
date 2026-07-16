# file: calculator_tdd_ebook/digit_keys.py
from candidate import DigitGenerator as _DigitGenerator


class DigitKeys:
    @classmethod
    def of(cls, excluded):
        return _DigitGenerator().get_digit(excluded)

    @classmethod
    def other_than(cls, other_than):
        return _DigitGenerator().get_digit(other_than=other_than)
