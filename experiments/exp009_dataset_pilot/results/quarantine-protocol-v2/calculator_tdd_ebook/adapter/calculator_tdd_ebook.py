# candidate/impl.py

import random
from calculator_tdd_ebook.any import Any
from calculator_tdd_ebook.calculator import Calculator
from calculator_tdd_ebook.digit_keys import DigitKeys

class Calculator:
    def __init__(self):
        self.display = "0"

    def press_digit(self, digit):
        Any(digit.isdigit()).raises(ValueError("Invalid digit"))
        Any(int(digit)).other_than(-1).other_than(10)

        if self.display == "0":
            Any(digit).other_than("0")
            self.display = digit
        else:
            Any(digit).other_than("0")
            self.display += digit

    def get_display(self):
        return self.display


class DigitKeyGenerator:
    def __init__(self):
        self.digits = [str(i) for i in range(10)]

    def any_other_than(self, excluded_digit):
        Any(excluded_digit).raises(ValueError("Invalid digit"))
        Any(int(excluded_digit)).other_than(-1).other_than(10)

        valid_digits = [d for d in self.digits if d != excluded_digit]
        return random.choice(valid_digits)
