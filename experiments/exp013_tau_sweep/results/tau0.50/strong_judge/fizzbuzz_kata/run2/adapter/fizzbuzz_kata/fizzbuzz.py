# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatch

from candidate import call_number as _call_number
from candidate import play_game as _play_game


class _NoArgument:
    pass


@singledispatch
def _print_fizz_buzz(value):
    return _call_number(value)


@_print_fizz_buzz.register
def _(value: _NoArgument):
    return _play_game()


def _print_fizz_buzz_adapter(value=_NoArgument()):
    return _print_fizz_buzz(value)


class FizzBuzz:
    print_fizz_buzz = staticmethod(_print_fizz_buzz_adapter)
    raises = staticmethod(_call_number)
