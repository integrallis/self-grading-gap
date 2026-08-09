# your complete test file
from solution import call_number, play_game

def test_call_number_returns_number_itself():
    # 1 is not divisible by 3 or 5
    assert call_number(1) == "1"

def test_call_number_returns_fizz_for_multiples_of_3():
    # 3 is divisible by 3 and not by 5
    assert call_number(3) == "Fizz"
    # 6 is divisible by 3 and not by 5
    assert call_number(6) == "Fizz"
    # 9 is divisible by 3 and not by 5
    assert call_number(9) == "Fizz"

def test_call_number_returns_buzz_for_multiples_of_5():
    # 5 is divisible by 5 and not by 3
    assert call_number(5) == "Buzz"
    # 10 is divisible by 5 and not by 3
    assert call_number(10) == "Buzz"
    # 100 is divisible by 5 and not by 3
    assert call_number(100) == "Buzz"

def test_call_number_returns_fizzbuzz_for_multiples_of_both():
    # 15 is divisible by both 3 and 5
    assert call_number(15) == "FizzBuzz"
    # 30 is divisible by both 3 and 5
    assert call_number(30) == "FizzBuzz"

def test_call_number_rejects_numbers_below_1():
    # 0 is below 1
    assert call_number(0) == "entered number is [0], which does not meet rule, entered number should be between 1 to 100."
    # -1 is below 1
    assert call_number(-1) == "entered number is [-1], which does not meet rule, entered number should be between 1 to 100."

def test_call_number_rejects_numbers_above_100():
    # 101 is above 100
    assert call_number(101) == "entered number is [101], which does not meet rule, entered number should be between 1 to 100."
    # 200 is above 100
    assert call_number(200) == "entered number is [200], which does not meet rule, entered number should be between 1 to 100."

def test_play_game_returns_full_sequence():
    # The full sequence from 1 to 100 according to FizzBuzz rules
    expected_output = "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz " \
                      "16 17 Fizz 19 Buzz Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz " \
                      "31 32 Fizz 34 Buzz Fizz 37 38 Fizz Buzz 41 Fizz 43 44 FizzBuzz " \
                      "46 47 Fizz 49 Buzz Fizz 52 53 Fizz Buzz 56 Fizz 58 59 FizzBuzz " \
                      "61 62 Fizz 64 Buzz Fizz 67 68 Fizz Buzz 71 Fizz 73 74 FizzBuzz " \
                      "76 77 Fizz 79 Buzz Fizz 82 83 Fizz Buzz 86 Fizz 88 89 FizzBuzz " \
                      "91 92 Fizz 94 Buzz Fizz 97 98 Fizz Buzz"
    assert play_game() == expected_output