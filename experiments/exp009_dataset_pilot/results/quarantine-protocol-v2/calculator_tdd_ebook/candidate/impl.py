# candidate/impl.py

import random

class Calculator:
    def __init__(self):
        self.display = "0"

    def press_digit(self, digit):
        if not digit.isdigit() or not (0 <= int(digit) <= 9):
            raise ValueError("Invalid digit")

        if self.display == "0":
            if digit == "0":
                return  # Display remains "0"
            else:
                self.display = digit
        else:
            if digit != "0":
                self.display += digit
            else:
                self.display += "0"

    def get_display(self):
        return self.display


class DigitKeyGenerator:
    def __init__(self):
        self.digits = [str(i) for i in range(10)]

    def any_other_than(self, excluded_digit):
        if not isinstance(excluded_digit, str) or not excluded_digit.isdigit() or not (0 <= int(excluded_digit) <= 9):
            raise NotImplementedError(f"other_than not implemented for {type(excluded_digit)}")

        valid_digits = [d for d in self.digits if d != excluded_digit]
        return random.choice(valid_digits)
