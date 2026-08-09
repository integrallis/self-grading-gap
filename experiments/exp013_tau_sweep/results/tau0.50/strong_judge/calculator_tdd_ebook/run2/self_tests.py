# test_calculator.py

import pytest
from solution import Calculator, DigitGenerator

def test_initial_display_is_zero():
    # A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"  # Expected: "0"

def test_digit_entry_non_zero():
    # A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    for digits in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
        for digit in digits:
            calculator.press_digit(digit)
        assert calculator.display() == ''.join(map(str, digits))  # Expected: concatenation of digits

def test_digit_entry_zero_only():
    # Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    for _ in range(5):  # Testing with multiple zero presses
        calculator.press_digit(0)
    assert calculator.display() == "0"  # Expected: "0"

def test_digit_entry_leading_zero():
    # A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calculator = Calculator()
    for digit in [0, 7]:
        calculator.press_digit(digit)
    assert calculator.display() == "7"  # Expected: "7"
    
def test_digit_entry_significant_zeros():
    # Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press_digit(2)  # Pressing 2
    calculator.press_digit(0)  # Pressing 0
    calculator.press_digit(3)  # Pressing 3
    assert calculator.display() == "203"  # Expected: "203"

def test_digit_generator_excludes_specified_digit():
    # Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitGenerator()
    excluded_digits = range(10)  # Valid digits are 0-9
    for excluded_digit in excluded_digits:
        result = generator.get_digit(other_than=excluded_digit)
        assert result != excluded_digit  # Expected: a digit that is not excluded
        assert result in excluded_digits  # Expected: result is a valid digit

def test_digit_generator_without_exclusion():
    # Asking for a digit key without exclusion should yield a valid digit key.
    generator = DigitGenerator()
    result = generator.get_digit()
    assert result in range(10)  # Expected: result is a valid digit

def test_digit_generator_invalid_type():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as exc_info:
        generator.get_digit(other_than="string")
    assert str(exc_info.value) == "other_than not implemented for <class 'str'>"  # Expected message

def test_digit_generator_invalid_non_digit_type():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as exc_info:
        generator.get_digit(other_than=3.14)  # Non-digit type
    assert "<class 'float'>" in str(exc_info.value)  # Check that the exception message includes the type