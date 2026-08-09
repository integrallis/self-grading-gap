# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatchmethod

from candidate import call_number, play_game


class _NoArgument:
    pass


_NO_ARGUMENT = _NoArgument()


class FizzBuzz:
    @singledispatchmethod
    def print_fizz_buzz(self, value=_NO_ARGUMENT):
        return call_number(value)

    @print_fizz_buzz.register
    def _(self, value: _NoArgument):
        return play_game()

    def raises(self, value):
        return call_number(value)
