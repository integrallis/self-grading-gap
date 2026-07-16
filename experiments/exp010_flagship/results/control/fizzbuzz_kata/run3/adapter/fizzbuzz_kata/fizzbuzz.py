# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatchmethod

from candidate import call_number, play_fizzbuzz


class _NoArgument:
    pass


_NO_ARGUMENT = _NoArgument()


class FizzBuzz:
    @singledispatchmethod
    def print_fizz_buzz(self, value):
        return call_number(value)

    @print_fizz_buzz.register
    def _(self, value: _NoArgument):
        return play_fizzbuzz()

    def print_fizz_buzz(self, value=_NO_ARGUMENT):
        return self._print_fizz_buzz(value)

    @singledispatchmethod
    def _print_fizz_buzz(self, value):
        return call_number(value)

    @_print_fizz_buzz.register
    def _(self, value: _NoArgument):
        return play_fizzbuzz()

    def raises(self, value):
        return call_number(value)
