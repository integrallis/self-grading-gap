import pytest
from solution import Calculator, DigitGenerator

def test_calculator_initial_display():
    # A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

def test_calculator_digit_entry_non_zero_start():
    # A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press('4')
    calculator.press('5')
    calculator.press('6')
    assert calculator.display() == "456"

def test_calculator_press_zero_only():
    # Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    for _ in range(10):  # Pressing zero 10 times
        calculator.press('0')
    assert calculator.display() == "0"

def test_calculator_leading_zero_replaced():
    # A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calculator = Calculator()
    calculator.press('0')
    calculator.press('7')
    assert calculator.display() == "7"

def test_calculator_significant_zeros():
    # Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press('3')
    calculator.press('0')
    calculator.press('2')
    assert calculator.display() == "302"

def test_digit_generator_excludes_digit():
    # Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitGenerator()
    for excluded_digit in '0123456789':
        generated = {generator.get_digit(excluded_digit) for _ in range(100)}
        assert excluded_digit not in generated
        assert all(digit in '0123456789' for digit in generated)

def test_digit_generator_invalid_type():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as exc_info:
        generator.get_digit("invalid")
    assert str(exc_info.value) == "other_than not implemented for <class 'str'>"

def test_digit_generator_non_text_invalid_type():
    # Asking for a value that is not a text input is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as exc_info:
        generator.get_digit(5)
    assert str(exc_info.value) == "other_than not implemented for <class 'int'>"