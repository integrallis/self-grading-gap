# file: lcd_digits/lcd_digits.py
from candidate import render_lcd


class LCDDigits:
    def get_digits(self, value):
        return render_lcd(value)
