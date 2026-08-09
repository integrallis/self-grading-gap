# test_calculator.py

import pytest
from solution import Calculator, RandomDigitGenerator

def test_calculator_initial_state():
    # AC-1.1: A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

def test_calculator_digit_entry_non_zero_start():
    # AC-2.1: A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press('1')
    calculator.press('0')
    calculator.press('5')
    assert calculator.display() == "105"  # "1" + "0" + "5"

def test_calculator_digit_entry_zero_only():
    # AC-2.2: Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    calculator.press('0')
    calculator.press('0')
    calculator.press('0')
    assert calculator.display() == "0"  # Only zeros pressed

def test_calculator_digit_entry_leading_zero():
    # AC-2.3: A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calculator = Calculator()
    calculator.press('0')
    calculator.press('5')
    assert calculator.display() == "5"  # Leading zero replaced by "5"

def test_calculator_digit_entry_significant_zeros():
    # AC-2.4: Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press('1')
    calculator.press('0')
    calculator.press('5')
    assert calculator.display() == "105"  # "1" + "0" + "5"

def test_random_digit_generator_excludes_digit():
    # AC-3.1: Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = RandomDigitGenerator()
    for excluded_digit in '0123456789':
        digit = generator.random_digit(excluded=excluded_digit)
        assert digit != excluded_digit and digit in '0123456789'  # Should not be excluded and must be a digit

def test_random_digit_generator_no_exclusion():
    # AC-3.1: Asking for a digit key without exclusion yields a valid digit key.
    generator = RandomDigitGenerator()
    digit = generator.random_digit()  # No excluded digit
    assert digit in '0123456789'  # Must be a digit

def test_random_digit_generator_invalid_type():
    # AC-3.2: Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = RandomDigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.random_digit(excluded="invalid")
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"  # Exact error message

def test_random_digit_generator_invalid_number_type():
    # AC-3.2: Asking for a value that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = RandomDigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.random_digit(excluded=42)  # Invalid type, should raise
    # Assert only that the error names the offending type, not that it matches an exact message format.
    assert "int" in str(excinfo.value)  # The message must mention the type 'int'