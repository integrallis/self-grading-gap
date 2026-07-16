# file: lcd_digits/lcd_digits.py
from candidate import render_number


class LCDDigits:
    def get_digits(self, value):
        return render_number(value)
