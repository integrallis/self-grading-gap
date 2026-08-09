import pytest

def test_spell_number_zero():
    # 0 is spelled "zero"
    assert spell_number(0) == "zero"

def test_spell_number_single_digits():
    # Single digits: 1 is spelled "one", 5 is spelled "five", 8 is spelled "eight"
    assert spell_number(1) == "one"
    assert spell_number(5) == "five"
    assert spell_number(8) == "eight"

def test_spell_number_ten():
    # 10 is spelled "ten"
    assert spell_number(10) == "ten"

def test_spell_number_teens():
    # Teens: 11 is spelled "eleven", 13 is spelled "thirteen", 18 is spelled "eighteen", 19 is spelled "nineteen"
    assert spell_number(11) == "eleven"
    assert spell_number(13) == "thirteen"
    assert spell_number(18) == "eighteen"
    assert spell_number(19) == "nineteen"

def test_spell_number_round_tens():
    # Round tens: 20 is "twenty", 30 is "thirty", 90 is "ninety"
    assert spell_number(20) == "twenty"
    assert spell_number(30) == "thirty"
    assert spell_number(90) == "ninety"

def test_spell_number_hyphenated_tens():
    # Hyphenated tens: 21 is "twenty-one", 77 is "seventy-seven", 99 is "ninety-nine"
    assert spell_number(21) == "twenty-one"
    assert spell_number(77) == "seventy-seven"
    assert spell_number(99) == "ninety-nine"

def test_spell_number_hundreds():
    # Hundreds: 100 is "one hundred", 303 is "three hundred three", 555 is "five hundred fifty-five"
    assert spell_number(100) == "one hundred"
    assert spell_number(303) == "three hundred three"
    assert spell_number(555) == "five hundred fifty-five"

def test_spell_number_hundreds_no_and():
    # No "and" between hundreds and remainder: 115 is "one hundred fifteen"
    assert spell_number(115) == "one hundred fifteen"

def test_spell_number_thousands():
    # Thousands: 1000 is "one thousand", 2000 is "two thousand"
    assert spell_number(1000) == "one thousand"
    assert spell_number(2000) == "two thousand"

def test_spell_number_thousands_with_remainder():
    # Thousands with remainder: 2400 is "two thousand four hundred", 3466 is "three thousand four hundred sixty-six"
    assert spell_number(2400) == "two thousand four hundred"
    assert spell_number(3466) == "three thousand four hundred sixty-six"

def test_spell_number_empty_hundreds():
    # Empty hundreds part: 5005 is "five thousand five"
    assert spell_number(5005) == "five thousand five"

def test_spell_number_maximum():
    # Largest supported number: 9999 is "nine thousand nine hundred ninety-nine"
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"

def test_spell_number_negative():
    # Negative number: should raise an error containing "must be in 0..9999"
    with pytest.raises(Exception, match=r"must be in 0..9999"):
        spell_number(-1)

def test_spell_number_too_large():
    # Number greater than 9999: should raise an error containing "must be in 0..9999"
    with pytest.raises(Exception, match=r"must be in 0..9999"):
        spell_number(10000)

def test_spell_number_structural_cases():
    # Additional valid structural cases: 101 is "one hundred one", 110 is "one hundred ten", 1001 is "one thousand one", 9000 is "nine thousand"
    assert spell_number(101) == "one hundred one"
    assert spell_number(110) == "one hundred ten"
    assert spell_number(1001) == "one thousand one"
    assert spell_number(9000) == "nine thousand"