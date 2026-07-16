# file: odd_even_kata/odd_even.py
from candidate import announce_number as _announce_number
from candidate import announce_range as _announce_range


class OddEven:
    print_odd_even = staticmethod(_announce_range)
    print_single_odd_even = staticmethod(_announce_number)
