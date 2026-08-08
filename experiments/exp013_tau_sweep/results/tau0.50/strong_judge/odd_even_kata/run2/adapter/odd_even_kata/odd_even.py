# file: odd_even_kata/odd_even.py
from candidate import announce_number, announce_range


class OddEven:
    def print_odd_even(self, start, end):
        return announce_range(start, end)

    def print_single_odd_even(self, number):
        return announce_number(number)
