# candidate/impl.py

import random

class Calculator:
    def __init__(self):
        self.display = "0"
    
    def press_digit(self, digit):
        if not digit.isdigit() or not (0 <= int(digit) <= 9):
            raise ValueError("Invalid digit")
        
        if self.display == "0" and digit == "0":
            return  # Do nothing, display remains "0"
        
        if self.display == "0" and digit != "0":
            self.display = digit
        elif self.display == "0":
            self.display = digit
        else:
            self.display += digit
            
        # Remove leading zeros
        self.display = str(int(self.display))
    
    def get_display(self):
        return self.display


class DigitGenerator:
    def __init__(self):
        self.digits = [str(i) for i in range(10)]

    def generate_digit(self, exclude=None):
        if exclude is not None and (not isinstance(exclude, str) or not exclude.isdigit() or not (0 <= int(exclude) <= 9)):
            raise NotImplementedError(f"other_than not implemented for {type(exclude)}")
        
        valid_digits = [d for d in self.digits if d != exclude]
        return random.choice(valid_digits)
