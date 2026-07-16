# your complete test file
import pytest
from solution import spell_number

def test_spell_number_zero():
    # 0 is spelled "zero"
    assert spell_number(0) == "zero"

def test_spell_number_single_digits():
    # 1 is "one", 2 is "two", ..., 9 is "nine"
    assert spell_number(1) == "one"
    assert spell_number(2) == "two"
    assert spell_number(3) == "three"
    assert spell_number(4) == "four"
    assert spell_number(5) == "five"
    assert spell_number(6) == "six"
    assert spell_number(7) == "seven"
    assert spell_number(8) == "eight"
    assert spell_number(9) == "nine"

def test_spell_number_teens():
    # 10 is "ten", 11 is "eleven", ..., 19 is "nineteen"
    assert spell_number(10) == "ten"
    assert spell_number(11) == "eleven"
    assert spell_number(12) == "twelve"
    assert spell_number(13) == "thirteen"
    assert spell_number(14) == "fourteen"
    assert spell_number(15) == "fifteen"
    assert spell_number(16) == "sixteen"
    assert spell_number(17) == "seventeen"
    assert spell_number(18) == "eighteen"
    assert spell_number(19) == "nineteen"

def test_spell_number_round_tens():
    # 20 is "twenty", ..., 90 is "ninety"
    assert spell_number(20) == "twenty"
    assert spell_number(30) == "thirty"
    assert spell_number(40) == "forty"
    assert spell_number(50) == "fifty"
    assert spell_number(60) == "sixty"
    assert spell_number(70) == "seventy"
    assert spell_number(80) == "eighty"
    assert spell_number(90) == "ninety"

def test_spell_number_hyphenated_compounds():
    # 21 is "twenty-one", ..., 99 is "ninety-nine"
    assert spell_number(21) == "twenty-one"
    assert spell_number(22) == "twenty-two"
    assert spell_number(77) == "seventy-seven"
    assert spell_number(99) == "ninety-nine"

def test_spell_number_hundreds():
    # 100 is "one hundred", 303 is "three hundred three", 555 is "five hundred fifty-five"
    assert spell_number(100) == "one hundred"
    assert spell_number(303) == "three hundred three"
    assert spell_number(555) == "five hundred fifty-five"
    assert spell_number(115) == "one hundred fifteen"

def test_spell_number_thousands():
    # 1000 is "one thousand", 2400 is "two thousand four hundred", 5005 is "five thousand five"
    assert spell_number(1000) == "one thousand"
    assert spell_number(2400) == "two thousand four hundred"
    assert spell_number(3466) == "three thousand four hundred sixty-six"
    assert spell_number(5005) == "five thousand five"
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"

def test_spell_number_negative():
    # Negative numbers must raise an error
    with pytest.raises(ValueError, match="must be in 0..9999"):
        spell_number(-1)

def test_spell_number_too_large():
    # Numbers greater than 9999 must raise an error
    with pytest.raises(ValueError, match="must be in 0..9999"):
        spell_number(10000)