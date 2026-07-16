import pytest
from solution import Calculator, DigitGenerator

def test_calculator_initial_display_zero():
    # A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

def test_calculator_digit_entry_non_zero():
    # A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press_digit('1')
    calculator.press_digit('2')
    calculator.press_digit('3')
    assert calculator.display() == "123"

    calculator = Calculator()
    calculator.press_digit('4')
    calculator.press_digit('5')
    calculator.press_digit('6')
    assert calculator.display() == "456"

    calculator = Calculator()
    calculator.press_digit('7')
    calculator.press_digit('8')
    calculator.press_digit('9')
    assert calculator.display() == "789"

def test_calculator_digit_entry_only_zero():
    # Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    calculator.press_digit('0')
    calculator.press_digit('0')
    calculator.press_digit('0')
    assert calculator.display() == "0"

def test_calculator_digit_entry_leading_zero():
    # A leading zero is replaced by the first non-zero digit: pressing zero then each digit from 1 to 9 reads that digit.
    for digit in '123456789':
        calculator = Calculator()
        calculator.press_digit('0')
        calculator.press_digit(digit)
        assert calculator.display() == digit  # Should read the non-zero digit

def test_calculator_digit_entry_significant_zeros():
    # Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press_digit('1')
    calculator.press_digit('0')
    calculator.press_digit('5')
    assert calculator.display() == "105"

    # Additional tests for significant trailing zeroes after non-zero digit
    calculator = Calculator()
    calculator.press_digit('1')
    calculator.press_digit('0')
    assert calculator.display() == "10"  # Should read "10"

    calculator = Calculator()
    calculator.press_digit('1')
    calculator.press_digit('0')
    calculator.press_digit('0')
    assert calculator.display() == "100"  # Should read "100"

def test_digit_generator_excludes_given_digit():
    # Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitGenerator()

    for excluded_digit in '0123456789':
        digit = generator.get_digit(excluded_digit)
        assert digit != excluded_digit
        assert digit in '0123456789'  # Valid digits excluding the excluded one

def test_digit_generator_not_implemented_for_non_digit():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit("string")
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"