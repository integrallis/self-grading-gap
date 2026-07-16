class Calculator:
    def __init__(self):
        self.current_display = "0"

    def press(self, digit):
        if self.current_display == "0" and digit != "0":
            self.current_display = digit
        elif self.current_display != "0":
            self.current_display += digit

    def display(self):
        return self.current_display

class DigitGenerator:
    def get_digit(self, excluded=None, other_than=None):
        if other_than is not None:
            raise NotImplementedError(f"other_than not implemented for {type(other_than)}")
        import random
        digits = [str(d) for d in range(10) if str(d) != excluded]
        return random.choice(digits)