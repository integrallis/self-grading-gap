# your complete test file
import pytest
from solution import spell_number

# US-1: Spelling numbers up to twenty

def test_zero():
    assert spell_number(0) == "zero"  # AC-1.1

def test_single_digits():
    assert spell_number(5) == "five"  # AC-1.1
    assert spell_number(8) == "eight"  # AC-1.1

def test_ten():
    assert spell_number(10) == "ten"  # AC-1.2

def test_teens():
    assert spell_number(13) == "thirteen"  # AC-1.2
    assert spell_number(19) == "nineteen"  # AC-1.2

# US-2: Spelling two-digit numbers

def test_round_tens():
    assert spell_number(20) == "twenty"  # AC-2.1
    assert spell_number(90) == "ninety"  # AC-2.1

def test_hyphenated_tens_units():
    assert spell_number(21) == "twenty-one"  # AC-2.2
    assert spell_number(77) == "seventy-seven"  # AC-2.2
    assert spell_number(99) == "ninety-nine"  # AC-2.2

# US-3: Spelling hundreds

def test_hundreds():
    assert spell_number(100) == "one hundred"  # AC-3.1
    assert spell_number(303) == "three hundred three"  # AC-3.2
    assert spell_number(555) == "five hundred fifty-five"  # AC-3.2
    assert spell_number(115) == "one hundred fifteen"  # AC-3.3

# US-4: Spelling thousands

def test_thousands():
    assert spell_number(1000) == "one thousand"  # AC-4.1
    assert spell_number(2000) == "two thousand"  # AC-4.1
    assert spell_number(2400) == "two thousand four hundred"  # AC-4.2
    assert spell_number(3466) == "three thousand four hundred sixty-six"  # AC-4.2
    assert spell_number(5005) == "five thousand five"  # AC-4.2
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"  # AC-4.3

# US-5: Rejecting numbers outside the range

def test_negative_number():
    with pytest.raises(Exception, match=r"must be in 0\.\.9999"):
        spell_number(-1)  # AC-5.1

def test_number_too_large():
    with pytest.raises(Exception, match=r"must be in 0\.\.9999"):
        spell_number(10000)  # AC-5.2

# Additional tests for lexical boundaries
def test_eleven():
    assert spell_number(11) == "eleven"  # additional test

def test_twelve():
    assert spell_number(12) == "twelve"  # additional test

def test_forty():
    assert spell_number(40) == "forty"  # additional test

def test_nine_hundred_ninety_nine():
    assert spell_number(999) == "nine hundred ninety-nine"  # additional test

def test_one_thousand_one():
    assert spell_number(1001) == "one thousand one"  # additional test