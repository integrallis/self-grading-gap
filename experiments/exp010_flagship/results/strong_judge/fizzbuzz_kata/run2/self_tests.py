# test_fizzbuzz.py

from solution import call_number, play_game

def test_call_number_returns_itself_for_numbers_not_divisible_by_3_or_5():
    assert call_number(1) == "1"  # 1 is not divisible by 3 or 5
    assert call_number(2) == "2"  # 2 is not divisible by 3 or 5
    assert call_number(4) == "4"  # 4 is not divisible by 3 or 5
    assert call_number(7) == "7"  # 7 is not divisible by 3 or 5
    assert call_number(8) == "8"  # 8 is not divisible by 3 or 5
    assert call_number(11) == "11"  # 11 is not divisible by 3 or 5

def test_call_number_returns_fizz_for_multiples_of_3_not_5():
    assert call_number(3) == "Fizz"  # 3 is a multiple of 3
    assert call_number(6) == "Fizz"  # 6 is a multiple of 3
    assert call_number(9) == "Fizz"  # 9 is a multiple of 3
    assert call_number(12) == "Fizz"  # 12 is a multiple of 3
    assert call_number(18) == "Fizz"  # 18 is a multiple of 3

def test_call_number_returns_buzz_for_multiples_of_5_not_3():
    assert call_number(5) == "Buzz"  # 5 is a multiple of 5
    assert call_number(10) == "Buzz"  # 10 is a multiple of 5
    assert call_number(20) == "Buzz"  # 20 is a multiple of 5
    assert call_number(25) == "Buzz"  # 25 is a multiple of 5
    assert call_number(100) == "Buzz"  # 100 is a multiple of 5

def test_call_number_returns_fizzbuzz_for_multiples_of_both():
    assert call_number(15) == "FizzBuzz"  # 15 is a multiple of both 3 and 5
    assert call_number(30) == "FizzBuzz"  # 30 is a multiple of both 3 and 5
    assert call_number(45) == "FizzBuzz"  # 45 is a multiple of both 3 and 5
    assert call_number(60) == "FizzBuzz"  # 60 is a multiple of both 3 and 5
    assert call_number(75) == "FizzBuzz"  # 75 is a multiple of both 3 and 5

def test_play_game_returns_correct_sequence():
    expected_output = "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz " \
                      "16 17 Fizz 19 Buzz Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz " \
                      "31 32 Fizz 34 Buzz Fizz 37 38 Fizz Buzz 41 Fizz 43 44 FizzBuzz " \
                      "46 47 Fizz 49 Buzz Fizz 52 53 Fizz Buzz 56 Fizz 58 59 FizzBuzz " \
                      "61 62 Fizz 64 Buzz Fizz 67 68 Fizz Buzz 71 Fizz 73 74 FizzBuzz " \
                      "76 77 Fizz 79 Buzz Fizz 82 83 Fizz Buzz 86 Fizz 88 89 FizzBuzz " \
                      "91 92 Fizz 94 Buzz Fizz 97 98 Fizz Buzz"  # 1 to 100 FizzBuzz sequence
    assert play_game() == expected_output

def test_call_number_refuses_numbers_below_1():
    assert call_number(0) == "entered number is [0], which does not meet rule, entered number should be between 1 to 100."  # 0 is below 1
    assert call_number(-1) == "entered number is [-1], which does not meet rule, entered number should be between 1 to 100."  # -1 is below 1

def test_call_number_refuses_numbers_above_100():
    assert call_number(101) == "entered number is [101], which does not meet rule, entered number should be between 1 to 100."  # 101 is above 100
    assert call_number(150) == "entered number is [150], which does not meet rule, entered number should be between 1 to 100."  # 150 is above 100