import pytest
from solution import spell_number

def test_spell_number_zero():
    assert spell_number(0) == "zero"  # AC-1.1: Zero is spelled "zero"

def test_spell_number_single_digits():
    assert spell_number(5) == "five"  # AC-1.1: Five is spelled "five"
    assert spell_number(8) == "eight"  # AC-1.1: Eight is spelled "eight"

def test_spell_number_ten():
    assert spell_number(10) == "ten"  # AC-1.2: Ten is spelled "ten"

def test_spell_number_teens():
    assert spell_number(13) == "thirteen"  # AC-1.2: Thirteen is spelled "thirteen"
    assert spell_number(19) == "nineteen"  # AC-1.2: Nineteen is spelled "nineteen"

def test_spell_number_tens():
    assert spell_number(20) == "twenty"  # AC-2.1: Twenty is spelled "twenty"
    assert spell_number(30) == "thirty"  # AC-2.1: Thirty is spelled "thirty"
    assert spell_number(90) == "ninety"  # AC-2.1: Ninety is spelled "ninety"

def test_spell_number_compound_tens():
    assert spell_number(21) == "twenty-one"  # AC-2.2: Twenty-one is spelled "twenty-one"
    assert spell_number(77) == "seventy-seven"  # AC-2.2: Seventy-seven is spelled "seventy-seven"
    assert spell_number(99) == "ninety-nine"  # AC-2.2: Ninety-nine is spelled "ninety-nine"

def test_spell_number_hundreds():
    assert spell_number(100) == "one hundred"  # AC-3.1: One hundred is spelled "one hundred"
    assert spell_number(303) == "three hundred three"  # AC-3.2: Three hundred three is spelled "three hundred three"
    assert spell_number(555) == "five hundred fifty-five"  # AC-3.2: Five hundred fifty-five is spelled "five hundred fifty-five"
    assert spell_number(115) == "one hundred fifteen"  # AC-3.2: One hundred fifteen is spelled "one hundred fifteen"

def test_spell_number_thousands():
    assert spell_number(1000) == "one thousand"  # AC-4.1: One thousand is spelled "one thousand"
    assert spell_number(2000) == "two thousand"  # AC-4.1: Two thousand is spelled "two thousand"
    assert spell_number(2400) == "two thousand four hundred"  # AC-4.2: Two thousand four hundred is spelled "two thousand four hundred"
    assert spell_number(3466) == "three thousand four hundred sixty-six"  # AC-4.2: Three thousand four hundred sixty-six is spelled "three thousand four hundred sixty-six"
    assert spell_number(5005) == "five thousand five"  # AC-4.2: Five thousand five is spelled "five thousand five"
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"  # AC-4.3: Nine thousand nine hundred ninety-nine is spelled "nine thousand nine hundred ninety-nine"

def test_spell_number_reject_negative():
    with pytest.raises(Exception) as exc_info:
        spell_number(-1)  # AC-5.1: Negative number must raise an error
    assert "must be in 0..9999" in str(exc_info.value)

def test_spell_number_reject_above_9999():
    with pytest.raises(Exception) as exc_info:
        spell_number(10000)  # AC-5.2: Number above 9999 must raise an error
    assert "must be in 0..9999" in str(exc_info.value)

def test_spell_number_additional_cases():
    assert spell_number(11) == "eleven"  # Additional test: Eleven is spelled "eleven"
    assert spell_number(42) == "forty-two"  # Additional test: Forty-two is spelled "forty-two"
    assert spell_number(101) == "one hundred one"  # Additional test: One hundred one is spelled "one hundred one"
    assert spell_number(999) == "nine hundred ninety-nine"  # Additional test: Nine hundred ninety-nine is spelled "nine hundred ninety-nine"
    assert spell_number(1001) == "one thousand one"  # Additional test: One thousand one is spelled "one thousand one"
    assert spell_number(1010) == "one thousand ten"  # Additional test: One thousand ten is spelled "one thousand ten"