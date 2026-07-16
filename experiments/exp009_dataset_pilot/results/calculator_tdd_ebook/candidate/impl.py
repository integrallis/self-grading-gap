# candidate/impl.py

import random

class Calculator:
    def __init__(self):
        self.display = "0"
        self.is_non_zero_entered = False

    def press_digit(self, digit):
        if not digit.isdigit() or len(digit) != 1:
            raise ValueError("Input must be a single digit string.")
        
        if self.display == "0" and digit != "0":
            self.display = digit
            self.is_non_zero_entered = True
        elif self.display == "0" and digit == "0":
            pass  # Display remains "0"
        elif self.is_non_zero_entered:
            self.display += digit
        else:
            self.display = digit

    def get_display(self):
        return self.display


class DigitGenerator:
    def __init__(self):
        self.digits = [str(i) for i in range(10)]

    def get_random_digit(self, exclude=None):
        if exclude is not None and not isinstance(exclude, str):
            raise NotImplementedError(f"other_than not implemented for {type(exclude)}")
        
        available_digits = [d for d in self.digits if d != exclude]
        return random.choice(available_digits)
