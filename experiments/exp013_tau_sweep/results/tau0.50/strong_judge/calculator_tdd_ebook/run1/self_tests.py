# test_calculator.py

import pytest
from solution import Calculator, DigitKeyGenerator

def test_calculator_initial_display():
    # When the calculator is created, it should display zero.
    calculator = Calculator()
    assert calculator.display() == "0"  # AC-1.1

@pytest.mark.parametrize("digits, expected", [
    ([1, 2], "12"),  # AC-2.1
    ([3, 4, 5], "345"),  # AC-2.1
    ([7, 8], "78"),  # AC-2.1
])
def test_calculator_digit_entry_non_zero_start(digits, expected):
    calculator = Calculator()
    for digit in digits:
        calculator.press_digit(digit)
    assert calculator.display() == expected  # AC-2.1

@pytest.mark.parametrize("count", [1, 2, 3, 4])  # AC-2.2
def test_calculator_digit_entry_zero_only(count):
    calculator = Calculator()
    for _ in range(count):
        calculator.press_digit(0)
    assert calculator.display() == "0"  # AC-2.2

def test_calculator_digit_entry_leading_zero():
    # Pressing 0 then 5 should display "5", not "05"
    calculator = Calculator()
    calculator.press_digit(0)
    calculator.press_digit(5)
    assert calculator.display() == "5"  # AC-2.3

def test_calculator_digit_entry_significant_zeros():
    # Pressing 1, then 0, then 5 should display "105"
    calculator = Calculator()
    calculator.press_digit(1)
    calculator.press_digit(0)
    calculator.press_digit(5)
    assert calculator.display() == "105"  # AC-2.4

@pytest.mark.parametrize("excluded", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # AC-3.1
def test_digit_key_generator_valid_key(excluded):
    generator = DigitKeyGenerator()
    valid_key = generator.get_digit_key(excluded)
    assert valid_key != excluded  # Must not be the excluded key
    assert valid_key in range(10)  # Valid digit key must be between 0 and 9

@pytest.mark.parametrize("invalid_input", [None, 10, -1, 3.14, object])  # AC-3.2
def test_digit_key_generator_invalid_type(invalid_input):
    # Asking for a value other than a digit key should raise a NotImplementedError
    generator = DigitKeyGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_key(invalid_input)
    assert str(excinfo.value) == f"other_than not implemented for {type(invalid_input)}"  # AC-3.2