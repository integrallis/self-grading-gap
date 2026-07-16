# candidate/impl.py

import random

class Calculator:
    def __init__(self):
        self.display = "0"

    def press_digit(self, digit):
        if not isinstance(digit, str) or not digit.isdigit() or len(digit) != 1:
            raise ValueError("Invalid digit. Must be a single character from '0' to '9'.")
        
        if self.display == "0":
            if digit == "0":
                self.display = "0"
            else:
                self.display = digit
        else:
            if digit != "0":
                self.display += digit
            else:
                self.display += "0"

    def get_display(self):
        return self.display


class DigitGenerator:
    def __init__(self, exclude_digit=None):
        self.exclude_digit = exclude_digit

    def get_digit(self):
        if self.exclude_digit is not None and (not isinstance(self.exclude_digit, str) or len(self.exclude_digit) != 1 or not self.exclude_digit.isdigit()):
            raise NotImplementedError(f"other_than not implemented for {type(self.exclude_digit)}")
        
        possible_digits = [str(i) for i in range(10) if str(i) != self.exclude_digit]
        return random.choice(possible_digits)
