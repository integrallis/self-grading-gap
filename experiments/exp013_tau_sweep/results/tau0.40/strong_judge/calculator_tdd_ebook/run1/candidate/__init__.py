class Calculator:
    def __init__(self):
        self.current_input = "0"
        self.is_leading_zero = True

    def press(self, digit):
        if digit not in '0123456789':
            raise ValueError("Invalid digit")

        if digit == '0':
            if self.is_leading_zero:
                self.current_input = "0"
            else:
                self.current_input += digit
        else:
            self.current_input = self.current_input.lstrip('0') + digit
            self.is_leading_zero = False

    def display(self):
        return self.current_input


class DigitGenerator:
    def get_digit_except(self, excluded_digit):
        if not isinstance(excluded_digit, str) or len(excluded_digit) != 1:
            raise NotImplementedError(f"other_than not implemented for {type(excluded_digit)}")
        digits = [d for d in '0123456789' if d != excluded_digit]
        return digits[0]  # or some random digit from the list