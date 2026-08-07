import pytest
from solution import Calculator, DigitGenerator

def test_calculator_initial_state():
    # AC-1.1: A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

def test_calculator_digit_entry_non_zero():
    # AC-2.1: A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press('3')
    calculator.press('5')
    assert calculator.display() == "35"

def test_calculator_digit_entry_only_zero():
    # AC-2.2: Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    calculator.press('0')
    assert calculator.display() == "0"  # Single zero press

    calculator.press('0')
    calculator.press('0')
    assert calculator.display() == "0"  # Three zero presses still displays one zero

def test_calculator_digit_entry_leading_zero():
    # AC-2.3: A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calculator = Calculator()
    calculator.press('0')
    calculator.press('5')
    assert calculator.display() == "5"

def test_calculator_digit_entry_significant_zeros():
    # AC-2.4: Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press('1')
    calculator.press('0')
    calculator.press('5')
    assert calculator.display() == "105"

def test_digit_generator_exclude_specific_digit():
    # AC-3.1: Asking for a digit key other than a given one always yields a valid digit key and never the excluded one, whichever digit key is excluded.
    generator = DigitGenerator()
    
    for excluded_digit in '0123456789':
        digit = generator.get_digit_except(excluded_digit)
        assert digit != excluded_digit and digit in '0123456789'

def test_digit_generator_invalid_type():
    # AC-3.2: Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type; for a plain text value the message is exactly "other_than not implemented for <class 'str'>".
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_except("invalid")
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"