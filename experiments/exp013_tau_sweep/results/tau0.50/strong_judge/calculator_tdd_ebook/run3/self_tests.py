# test_calculator.py

import pytest
from solution import Calculator, DigitGenerator

def test_switch_on_state():
    # AC-1.1: A freshly created calculator displays zero.
    calc = Calculator()
    assert calc.display == "0"  # Display should be "0" on creation

def test_digit_entry_non_zero_start():
    # AC-2.1: A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calc = Calculator()
    calc.press_digit('1')
    calc.press_digit('2')
    assert calc.display == "12"  # "1" + "2" = "12"

def test_digit_entry_zero_only():
    # AC-2.2: Pressing only the zero key, any number of times, displays a single zero.
    calc = Calculator()
    calc.press_digit('0')
    calc.press_digit('0')
    calc.press_digit('0')
    assert calc.display == "0"  # Multiple "0"s should still be "0"

def test_digit_entry_leading_zero():
    # AC-2.3: A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calc = Calculator()
    calc.press_digit('0')
    calc.press_digit('5')
    assert calc.display == "5"  # Leading "0" is ignored, "5" is displayed

def test_digit_entry_significant_zeros():
    # AC-2.4: Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calc = Calculator()
    calc.press_digit('1')
    calc.press_digit('0')
    calc.press_digit('5')
    assert calc.display == "105"  # "1" + "0" + "5" = "105"

def test_digit_generator_excludes_digit():
    # AC-3.1: Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitGenerator()
    for excluded_digit in '0123456789':
        generated_digit = generator.get_digit(excluded_digit)
        assert generated_digit != excluded_digit  # Generated digit must not be the excluded digit
        assert generated_digit in '0123456789'  # Generated digit must be a valid digit

def test_digit_generator_invalid_type_str():
    # AC-3.2: Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit('string')
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"  # Check the exact error message

def test_digit_generator_invalid_type_int():
    # AC-3.2: Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit(1)
    assert str(excinfo.value) == "other_than not implemented for <class 'int'>"  # Check the exact error message