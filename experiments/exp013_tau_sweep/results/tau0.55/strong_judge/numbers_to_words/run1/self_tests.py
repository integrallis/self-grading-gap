# test_solution.py

import pytest
import re  # Importing re for regex escaping

# US-1: Spelling numbers up to twenty
def test_spell_number_zero():
    assert spell_number(0) == "zero"  # Zero is spelled "zero".

def test_spell_number_single_digits():
    assert spell_number(1) == "one"  # One is spelled "one".
    assert spell_number(5) == "five"  # Five is spelled "five".
    assert spell_number(8) == "eight"  # Eight is spelled "eight".
    assert spell_number(9) == "nine"  # Nine is spelled "nine".

def test_spell_number_tens():
    assert spell_number(10) == "ten"  # Ten is spelled "ten".
    assert spell_number(11) == "eleven"  # Eleven is spelled "eleven".
    assert spell_number(12) == "twelve"  # Twelve is spelled "twelve".
    assert spell_number(13) == "thirteen"  # Thirteen is spelled "thirteen".
    assert spell_number(19) == "nineteen"  # Nineteen is spelled "nineteen".

# US-2: Spelling two-digit numbers
def test_spell_number_round_tens():
    assert spell_number(20) == "twenty"  # Twenty is spelled "twenty".
    assert spell_number(30) == "thirty"  # Thirty is spelled "thirty".
    assert spell_number(90) == "ninety"  # Ninety is spelled "ninety".

def test_spell_number_hyphenated_tens():
    assert spell_number(21) == "twenty-one"  # Twenty-one is spelled "twenty-one".
    assert spell_number(31) == "thirty-one"  # Thirty-one is spelled "thirty-one".
    assert spell_number(77) == "seventy-seven"  # Seventy-seven is spelled "seventy-seven".
    assert spell_number(89) == "eighty-nine"  # Eighty-nine is spelled "eighty-nine".
    assert spell_number(99) == "ninety-nine"  # Ninety-nine is spelled "ninety-nine".

# US-3: Spelling hundreds
def test_spell_number_hundreds():
    assert spell_number(100) == "one hundred"  # One hundred is spelled "one hundred".
    assert spell_number(303) == "three hundred three"  # Three hundred three is spelled "three hundred three".
    assert spell_number(555) == "five hundred fifty-five"  # Five hundred fifty-five is spelled "five hundred fifty-five".
    assert spell_number(115) == "one hundred fifteen"  # One hundred fifteen is spelled "one hundred fifteen".

# US-4: Spelling thousands
def test_spell_number_thousands():
    assert spell_number(1000) == "one thousand"  # One thousand is spelled "one thousand".
    assert spell_number(2000) == "two thousand"  # Two thousand is spelled "two thousand".
    assert spell_number(2400) == "two thousand four hundred"  # Two thousand four hundred is spelled "two thousand four hundred".
    assert spell_number(3466) == "three thousand four hundred sixty-six"  # Three thousand four hundred sixty-six is spelled "three thousand four hundred sixty-six".
    assert spell_number(5005) == "five thousand five"  # Five thousand five is spelled "five thousand five".
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"  # Nine thousand nine hundred ninety-nine is spelled "nine thousand nine hundred ninety-nine".

# US-5: Rejecting numbers outside the range
def test_spell_number_negative():
    with pytest.raises(Exception) as excinfo:  # Expecting any exception
        spell_number(-1)  # Negative number should raise an error.
    assert "must be in 0..9999" in str(excinfo.value)  # Checking the error message.

def test_spell_number_too_high():
    with pytest.raises(Exception) as excinfo:  # Expecting any exception
        spell_number(10000)  # Number greater than 9999 should raise an error.
    assert "must be in 0..9999" in str(excinfo.value)  # Checking the error message.