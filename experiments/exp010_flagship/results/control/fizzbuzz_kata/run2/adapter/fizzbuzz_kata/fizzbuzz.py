# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatch

from candidate import call_out_number as _call_out_number
from candidate import play_fizzbuzz_game as _play_fizzbuzz_game


class _Missing:
    pass


_missing = _Missing()


@singledispatch
def _print_fizz_buzz(value):
    return _call_out_number(value)


@_print_fizz_buzz.register(_Missing)
def _print_fizz_buzz_missing(value):
    return _play_fizzbuzz_game()


def _print_fizz_buzz_adapter(value=_missing):
    return _print_fizz_buzz(value)


class FizzBuzz:
    print_fizz_buzz = staticmethod(_print_fizz_buzz_adapter)
    raises = staticmethod(_call_out_number)
