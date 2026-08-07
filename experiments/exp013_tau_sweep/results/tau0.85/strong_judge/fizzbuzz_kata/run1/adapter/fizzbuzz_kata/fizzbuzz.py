# file: fizzbuzz_kata/fizzbuzz.py
from candidate import call_out_number, play_fizzbuzz_game


class FizzBuzz:
    print_fizz_buzz = staticmethod(play_fizzbuzz_game)
    raises = staticmethod(call_out_number)
