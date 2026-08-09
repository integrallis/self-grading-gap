# file: lcd_digits/lcd_digits.py
from candidate import render_lcd_digit


class LCDDigits:
    def get_digits(self, number):
        return render_lcd_digit(number)
