# your complete test file
from solution import call_number, play_fizzbuzz

def test_call_number_returns_number_itself_for_non_multiples():
    assert call_number(1) == "1"  # AC-1.1
    assert call_number(2) == "2"  # AC-1.1
    assert call_number(4) == "4"  # AC-1.1
    assert call_number(7) == "7"  # AC-1.1
    assert call_number(8) == "8"  # AC-1.1
    assert call_number(14) == "14"  # AC-1.1
    assert call_number(16) == "16"  # AC-1.1
    assert call_number(19) == "19"  # AC-1.1
    assert call_number(22) == "22"  # AC-1.1
    assert call_number(29) == "29"  # AC-1.1

def test_call_number_returns_fizz_for_multiples_of_3():
    assert call_number(3) == "Fizz"  # AC-1.2
    assert call_number(6) == "Fizz"  # AC-1.2
    assert call_number(9) == "Fizz"  # AC-1.2
    assert call_number(12) == "Fizz"  # AC-1.2
    assert call_number(18) == "Fizz"  # AC-1.2
    assert call_number(21) == "Fizz"  # AC-1.2
    assert call_number(24) == "Fizz"  # AC-1.2
    assert call_number(27) == "Fizz"  # AC-1.2
    assert call_number(30) == "Fizz"  # AC-1.4

def test_call_number_returns_buzz_for_multiples_of_5():
    assert call_number(5) == "Buzz"  # AC-1.3
    assert call_number(10) == "Buzz"  # AC-1.3
    assert call_number(20) == "Buzz"  # AC-1.3
    assert call_number(25) == "Buzz"  # AC-1.3
    assert call_number(35) == "Buzz"  # AC-1.3
    assert call_number(40) == "Buzz"  # AC-1.3
    assert call_number(50) == "Buzz"  # AC-1.3
    assert call_number(55) == "Buzz"  # AC-1.3
    assert call_number(100) == "Buzz"  # AC-1.3

def test_call_number_returns_fizzbuzz_for_multiples_of_both():
    assert call_number(15) == "FizzBuzz"  # AC-1.4
    assert call_number(30) == "FizzBuzz"  # AC-1.4
    assert call_number(45) == "FizzBuzz"  # AC-1.4
    assert call_number(60) == "FizzBuzz"  # AC-1.4
    assert call_number(75) == "FizzBuzz"  # AC-1.4
    assert call_number(90) == "FizzBuzz"  # AC-1.4

def test_call_number_rejects_numbers_below_1():
    assert call_number(0) == "entered number is [0], which does not meet rule, entered number should be between 1 to 100."  # AC-3.1
    assert call_number(-1) == "entered number is [-1], which does not meet rule, entered number should be between 1 to 100."  # AC-3.1

def test_call_number_rejects_numbers_above_100():
    assert call_number(101) == "entered number is [101], which does not meet rule, entered number should be between 1 to 100."  # AC-3.1
    assert call_number(200) == "entered number is [200], which does not meet rule, entered number should be between 1 to 100."  # AC-3.1

def test_play_fizzbuzz_returns_full_sequence():
    expected_output = "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz 31 32 Fizz 34 Buzz Fizz 37 38 Fizz Buzz 41 Fizz 43 44 FizzBuzz 46 47 Fizz 49 Buzz Fizz 52 53 Fizz Buzz 56 Fizz 58 59 FizzBuzz 61 62 Fizz 64 Buzz Fizz 67 68 Fizz Buzz 71 Fizz 73 74 FizzBuzz 76 77 Fizz 79 Buzz Fizz 82 83 Fizz Buzz 86 Fizz 88 89 FizzBuzz 91 92 Fizz 94 Buzz Fizz 97 98 Fizz Buzz"
    assert play_fizzbuzz() == expected_output  # AC-2.1