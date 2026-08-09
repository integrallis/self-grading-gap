# file: fizzbuzz_kata/fizzbuzz.py
from candidate import call_out_number
from candidate import play_fizzbuzz_game


class FizzBuzz:
    @staticmethod
    def print_fizz_buzz(*arguments):
        return {
            False: play_fizzbuzz_game,
            True: call_out_number,
        }.get(bool(arguments))(*arguments)

    raises = staticmethod(call_out_number)
