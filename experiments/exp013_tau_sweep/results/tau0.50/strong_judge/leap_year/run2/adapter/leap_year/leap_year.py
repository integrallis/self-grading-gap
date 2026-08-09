# file: leap_year/leap_year.py
from candidate import is_leap_year as _is_leap_year


class LeapYear:
    is_leap_year = staticmethod(_is_leap_year)
