import pytest
from solution import number_to_words

def test_zero():
    assert number_to_words(0) == "zero"  # AC-1.1

def test_single_digits():
    assert number_to_words(5) == "five"  # AC-1.1
    assert number_to_words(8) == "eight"  # AC-1.1

def test_ten():
    assert number_to_words(10) == "ten"  # AC-1.2

def test_teens():
    assert number_to_words(13) == "thirteen"  # AC-1.2
    assert number_to_words(19) == "nineteen"  # AC-1.2

def test_round_tens():
    assert number_to_words(20) == "twenty"  # AC-2.1
    assert number_to_words(90) == "ninety"  # AC-2.1

def test_hyphenated_tens():
    assert number_to_words(21) == "twenty-one"  # AC-2.2
    assert number_to_words(77) == "seventy-seven"  # AC-2.2
    assert number_to_words(99) == "ninety-nine"  # AC-2.2

def test_hundreds():
    assert number_to_words(100) == "one hundred"  # AC-3.1
    assert number_to_words(303) == "three hundred three"  # AC-3.2
    assert number_to_words(555) == "five hundred fifty-five"  # AC-3.2
    assert number_to_words(115) == "one hundred fifteen"  # AC-3.2

def test_hundreds_no_and():
    assert number_to_words(300) == "three hundred"  # AC-3.3
    assert number_to_words(400) == "four hundred"  # AC-3.3

def test_thousands():
    assert number_to_words(1000) == "one thousand"  # AC-4.1
    assert number_to_words(2000) == "two thousand"  # AC-4.1
    assert number_to_words(2400) == "two thousand four hundred"  # AC-4.2
    assert number_to_words(3466) == "three thousand four hundred sixty-six"  # AC-4.2
    assert number_to_words(5005) == "five thousand five"  # AC-4.2
    assert number_to_words(9999) == "nine thousand nine hundred ninety-nine"  # AC-4.3

def test_negative_number():
    with pytest.raises(BaseException, match=r"must be in 0\.\.9999"):
        number_to_words(-1)  # AC-5.1

def test_number_too_large():
    with pytest.raises(BaseException, match=r"must be in 0\.\.9999"):
        number_to_words(10000)  # AC-5.2