# file: odd_even_kata/odd_even.py
from candidate import announce_number as _announce_number
from candidate import announce_range as _announce_range


class OddEven:
    def print_odd_even(self, start, end):
        return _announce_range(start, end)

    def print_single_odd_even(self, number):
        return _announce_number(number)
