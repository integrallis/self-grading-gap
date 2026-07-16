class Calculator:
    def __init__(self):
        self.current_display = "0"

    def press(self, digit):
        if digit not in '0123456789':
            raise NotImplementedError(f"{digit} not implemented for digit input")
        if self.current_display == "0":
            self.current_display = digit if digit != '0' else "0"
        else:
            self.current_display += digit

    def display(self):
        return self.current_display

class DigitGenerator:
    def get_digit(self, excluded=None):
        if excluded is not None and not isinstance(excluded, str):
            raise NotImplementedError(f"other_than not implemented for {type(excluded)}")
        import random
        digits = [d for d in '0123456789' if d != excluded]
        return random.choice(digits)