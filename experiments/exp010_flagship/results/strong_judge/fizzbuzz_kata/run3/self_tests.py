# your complete test file
from solution import call_out_number, play_fizzbuzz

def test_call_out_number_returns_number_itself():
    assert call_out_number(1) == "1"  # 1 is not divisible by 3 or 5
    assert call_out_number(2) == "2"  # 2 is not divisible by 3 or 5
    assert call_out_number(4) == "4"  # 4 is not divisible by 3 or 5
    assert call_out_number(7) == "7"  # 7 is not divisible by 3 or 5

def test_call_out_number_returns_fizz():
    assert call_out_number(3) == "Fizz"  # 3 is a multiple of 3
    assert call_out_number(6) == "Fizz"  # 6 is a multiple of 3
    assert call_out_number(9) == "Fizz"  # 9 is a multiple of 3
    assert call_out_number(12) == "Fizz"  # 12 is a multiple of 3

def test_call_out_number_returns_buzz():
    assert call_out_number(5) == "Buzz"  # 5 is a multiple of 5
    assert call_out_number(10) == "Buzz"  # 10 is a multiple of 5
    assert call_out_number(20) == "Buzz"  # 20 is a multiple of 5
    assert call_out_number(100) == "Buzz"  # 100 is a multiple of 5

def test_call_out_number_returns_fizzbuzz():
    assert call_out_number(15) == "FizzBuzz"  # 15 is a multiple of both 3 and 5
    assert call_out_number(30) == "FizzBuzz"  # 30 is a multiple of both 3 and 5
    assert call_out_number(45) == "FizzBuzz"  # 45 is a multiple of both 3 and 5
    assert call_out_number(60) == "FizzBuzz"  # 60 is a multiple of both 3 and 5

def test_call_out_number_refuses_invalid_numbers():
    assert call_out_number(0) == "entered number is [0], which does not meet rule, entered number should be between 1 to 100."  # 0 is below 1
    assert call_out_number(-1) == "entered number is [-1], which does not meet rule, entered number should be between 1 to 100."  # -1 is below 1
    assert call_out_number(101) == "entered number is [101], which does not meet rule, entered number should be between 1 to 100."  # 101 is above 100

def test_play_fizzbuzz_returns_full_sequence():
    expected_output = "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz 21 Fizz 23 24 Fizz Buzz 26 27 Fizz 29 Buzz 31 32 Fizz 34 Buzz 36 37 Fizz 39 Buzz 41 Fizz 43 44 FizzBuzz 46 47 Fizz 49 Buzz 51 Fizz 53 54 Fizz Buzz 56 57 Fizz 59 Buzz 61 62 Fizz 64 Buzz 66 67 Fizz 69 Buzz 71 Fizz 73 74 FizzBuzz 76 77 Fizz 79 Buzz 81 Fizz 83 84 Fizz Buzz 86 87 Fizz 89 Buzz 91 92 Fizz 94 Buzz Fizz 97 98 Fizz Buzz"
    assert play_fizzbuzz() == expected_output  # Full sequence from 1 to 100 according to the game's rules