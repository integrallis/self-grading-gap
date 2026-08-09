# your complete test file
import pytest
from solution import *

def test_zero():
    assert number_to_words(0) == "zero"  # AC-1.1

def test_single_digits():
    assert number_to_words(5) == "five"  # AC-1.1
    assert number_to_words(8) == "eight"  # AC-1.1
    assert number_to_words(1) == "one"  # AC-1.1
    assert number_to_words(9) == "nine"  # AC-1.1

def test_tens():
    assert number_to_words(10) == "ten"  # AC-1.2
    assert number_to_words(13) == "thirteen"  # AC-1.2
    assert number_to_words(19) == "nineteen"  # AC-1.2

def test_round_tens():
    assert number_to_words(20) == "twenty"  # AC-2.1
    assert number_to_words(30) == "thirty"  # AC-2.1
    assert number_to_words(90) == "ninety"  # AC-2.1

def test_compound_tens():
    assert number_to_words(21) == "twenty-one"  # AC-2.2
    assert number_to_words(77) == "seventy-seven"  # AC-2.2
    assert number_to_words(99) == "ninety-nine"  # AC-2.2

def test_hundreds():
    assert number_to_words(100) == "one hundred"  # AC-3.1
    assert number_to_words(303) == "three hundred three"  # AC-3.2
    assert number_to_words(555) == "five hundred fifty-five"  # AC-3.2
    assert number_to_words(115) == "one hundred fifteen"  # AC-3.2

def test_hundreds_without_and():
    assert number_to_words(200) == "two hundred"  # AC-3.1
    assert number_to_words(456) == "four hundred fifty-six"  # AC-3.2

def test_thousands():
    assert number_to_words(1000) == "one thousand"  # AC-4.1
    assert number_to_words(2000) == "two thousand"  # AC-4.1
    assert number_to_words(2400) == "two thousand four hundred"  # AC-4.2
    assert number_to_words(3466) == "three thousand four hundred sixty-six"  # AC-4.2
    assert number_to_words(5005) == "five thousand five"  # AC-4.2
    assert number_to_words(9999) == "nine thousand nine hundred ninety-nine"  # AC-4.3

def test_reject_negative_numbers():
    with pytest.raises(Exception, match=r"must be in 0\.\.9999"):
        number_to_words(-1)  # AC-5.1

def test_reject_numbers_greater_than_9999():
    with pytest.raises(Exception, match=r"must be in 0\.\.9999"):
        number_to_words(10000)  # AC-5.2