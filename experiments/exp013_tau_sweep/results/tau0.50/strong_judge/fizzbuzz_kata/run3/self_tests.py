# test_solution.py

from solution import call_out_number, play_game

def test_call_out_number_not_divisible_by_3_or_5():
    # 1 is called as itself
    assert call_out_number(1) == "1"
    # 2 is called as itself
    assert call_out_number(2) == "2"
    # 4 is called as itself
    assert call_out_number(4) == "4"

def test_call_out_number_divisible_by_3():
    # 3 is called "Fizz"
    assert call_out_number(3) == "Fizz"
    # 6 is called "Fizz"
    assert call_out_number(6) == "Fizz"
    # 9 is called "Fizz"
    assert call_out_number(9) == "Fizz"

def test_call_out_number_divisible_by_5():
    # 5 is called "Buzz"
    assert call_out_number(5) == "Buzz"
    # 10 is called "Buzz"
    assert call_out_number(10) == "Buzz"
    # 100 is called "Buzz"
    assert call_out_number(100) == "Buzz"

def test_call_out_number_divisible_by_both_3_and_5():
    # 15 is called "FizzBuzz"
    assert call_out_number(15) == "FizzBuzz"
    # 30 is called "FizzBuzz"
    assert call_out_number(30) == "FizzBuzz"

def test_play_game():
    # The full sequence is produced
    expected_output = "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz " \
                      "16 17 Fizz 19 Buzz Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz " \
                      "31 32 Fizz 34 Buzz Fizz 37 38 Fizz Buzz 41 Fizz 43 44 FizzBuzz " \
                      "46 47 Fizz 49 Buzz Fizz 52 53 Fizz Buzz 56 Fizz 58 59 FizzBuzz " \
                      "61 62 Fizz 64 Buzz Fizz 67 68 Fizz Buzz 71 Fizz 73 74 FizzBuzz " \
                      "76 77 Fizz 79 Buzz Fizz 82 83 Fizz Buzz 86 Fizz 88 89 FizzBuzz " \
                      "91 92 Fizz 94 Buzz Fizz 97 98 Fizz Buzz"
    assert play_game() == expected_output

def test_call_out_number_below_1():
    # 0 is rejected with a specific message
    assert call_out_number(0) == "entered number is [0], which does not meet rule, entered number should be between 1 to 100."
    # -1 is rejected with a specific message
    assert call_out_number(-1) == "entered number is [-1], which does not meet rule, entered number should be between 1 to 100."

def test_call_out_number_above_100():
    # 101 is rejected with a specific message
    assert call_out_number(101) == "entered number is [101], which does not meet rule, entered number should be between 1 to 100."