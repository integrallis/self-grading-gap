# file: calculator_tdd_ebook/digit_keys.py
from candidate import DigitGenerator


class DigitKeys(DigitGenerator):
    def other_than(self, digit):
        return self.get_digit(digit)
