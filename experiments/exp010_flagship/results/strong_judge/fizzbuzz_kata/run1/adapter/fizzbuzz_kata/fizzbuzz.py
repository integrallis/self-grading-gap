# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatchmethod as _singledispatchmethod
from candidate import call_number as _call_number
from candidate import play_game as _play_game


class FizzBuzz:
    @_singledispatchmethod
    def print_fizz_buzz(self, number=None):
        return _call_number(number)

    @print_fizz_buzz.register(type(None))
    def _(self, number):
        return _play_game()

    def raises(self, number):
        return _call_number(number)
