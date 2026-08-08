# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatch

from candidate import call_out_number, play_fizzbuzz


class _Missing:
    pass


@singledispatch
def _print_fizz_buzz(number=_Missing()):
    return play_fizzbuzz()


@_print_fizz_buzz.register
def _(number: int):
    return call_out_number(number)


class FizzBuzz:
    print_fizz_buzz = staticmethod(_print_fizz_buzz)
    raises = staticmethod(call_out_number)
