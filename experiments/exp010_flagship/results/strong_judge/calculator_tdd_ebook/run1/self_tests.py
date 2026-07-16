# test_calculator.py

import pytest
from solution import Calculator, DigitKeyGenerator

def test_initial_display_is_zero():
    # A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

@pytest.mark.parametrize("digits, expected", [
    ([1, 2, 3], "123"),  # Non-zero leading concatenation: "1" + "2" + "3"
    ([4, 5, 6], "456"),  # Another non-zero leading concatenation: "4" + "5" + "6"
    ([7, 8, 9], "789"),  # Another non-zero leading concatenation: "7" + "8" + "9"
])
def test_digit_entry_non_zero(digits, expected):
    # A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    for digit in digits:
        calculator.press_digit(digit)
    assert calculator.display() == expected

def test_digit_entry_zero_only_one_press():
    # Pressing only the zero key once displays a single zero.
    calculator = Calculator()
    calculator.press_digit(0)
    assert calculator.display() == "0"

def test_digit_entry_zero_only_multiple_presses():
    # Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    for _ in range(5):  # Press zero five times
        calculator.press_digit(0)
    assert calculator.display() == "0"

@pytest.mark.parametrize("first_digit, expected", [
    (5, "5"),  # Leading zero replaced by first non-zero digit
    (3, "3"),  # Another leading zero replaced
])
def test_digit_entry_leading_zero(first_digit, expected):
    calculator = Calculator()
    calculator.press_digit(0)  # Leading zero
    calculator.press_digit(first_digit)
    assert calculator.display() == expected

def test_digit_entry_after_non_zero():
    # Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press_digit(1)
    calculator.press_digit(0)
    calculator.press_digit(5)
    assert calculator.display() == "105"

@pytest.mark.parametrize("excluded_digit", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_digit_key_generator_excludes_digit(excluded_digit):
    # Asking for a digit key other than a given one always yields a valid digit key and never the excluded one, whichever digit key is excluded.
    generator = DigitKeyGenerator()
    generated_key = generator.get_digit_key(excluded_digit)
    assert generated_key != excluded_digit
    assert 0 <= generated_key <= 9  # Ensure generated key is a valid digit key

def test_digit_key_generator_refuses_invalid_type():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitKeyGenerator()
    with pytest.raises(NotImplementedError) as exc:
        generator.get_digit_key("invalid")
    assert str(exc.value) == "other_than not implemented for <class 'str'>"