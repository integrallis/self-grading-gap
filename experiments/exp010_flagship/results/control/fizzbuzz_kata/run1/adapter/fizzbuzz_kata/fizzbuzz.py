# file: fizzbuzz_kata/fizzbuzz.py
from functools import singledispatch

from candidate import call_out_number, play_fizzbuzz_game


class _NoNumber:
    pass


def _print_fizz_buzz(number=_NoNumber()):
    return call_out_number(number)


_print_fizz_buzz = singledispatch(_print_fizz_buzz)


def _print_fizz_buzz_without_number(number):
    return play_fizzbuzz_game()


_print_fizz_buzz.register(_NoNumber, _print_fizz_buzz_without_number)


class FizzBuzz:
    print_fizz_buzz = staticmethod(_print_fizz_buzz)
    raises = staticmethod(call_out_number)
