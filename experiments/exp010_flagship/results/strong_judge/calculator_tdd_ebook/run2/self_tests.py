# test_calculator.py

import pytest
from solution import Calculator, DigitGenerator

def test_switch_on_state():
    # A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display == "0"

def test_digit_entry_non_zero_start_1():
    # A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press_digit(1)  # "1"
    assert calculator.display == "1"

def test_digit_entry_non_zero_start_2():
    calculator = Calculator()
    calculator.press_digit(2)  # "2"
    assert calculator.display == "2"

def test_digit_entry_non_zero_start_3():
    calculator = Calculator()
    calculator.press_digit(3)  # "3"
    assert calculator.display == "3"

def test_digit_entry_non_zero_start_4():
    calculator = Calculator()
    calculator.press_digit(4)  # "4"
    assert calculator.display == "4"

def test_digit_entry_non_zero_start_5():
    calculator = Calculator()
    calculator.press_digit(5)  # "5"
    assert calculator.display == "5"

def test_digit_entry_non_zero_start_6():
    calculator = Calculator()
    calculator.press_digit(6)  # "6"
    assert calculator.display == "6"

def test_digit_entry_non_zero_start_7():
    calculator = Calculator()
    calculator.press_digit(7)  # "7"
    assert calculator.display == "7"

def test_digit_entry_non_zero_start_8():
    calculator = Calculator()
    calculator.press_digit(8)  # "8"
    assert calculator.display == "8"

def test_digit_entry_non_zero_start_9():
    calculator = Calculator()
    calculator.press_digit(9)  # "9"
    assert calculator.display == "9"

def test_digit_entry_zero_only():
    # Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    calculator.press_digit(0)  # "0"
    calculator.press_digit(0)  # "0"
    assert calculator.display == "0"

def test_digit_entry_leading_zero():
    # A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calculator = Calculator()
    calculator.press_digit(0)  # "0"
    calculator.press_digit(5)  # "5"
    assert calculator.display == "5"

def test_digit_entry_zero_after_non_zero():
    # Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press_digit(1)  # "1"
    calculator.press_digit(0)  # "10"
    calculator.press_digit(5)  # "105"
    assert calculator.display == "105"

def test_digit_generator_excludes_digit_0():
    # Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitGenerator()
    excluded_digit = 0
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 0
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_1():
    generator = DigitGenerator()
    excluded_digit = 1
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 1
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_2():
    generator = DigitGenerator()
    excluded_digit = 2
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 2
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_3():
    generator = DigitGenerator()
    excluded_digit = 3
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 3
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_4():
    generator = DigitGenerator()
    excluded_digit = 4
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 4
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_5():
    generator = DigitGenerator()
    excluded_digit = 5
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 5
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_6():
    generator = DigitGenerator()
    excluded_digit = 6
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 6
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_7():
    generator = DigitGenerator()
    excluded_digit = 7
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 7
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_8():
    generator = DigitGenerator()
    excluded_digit = 8
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 8
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_excludes_digit_9():
    generator = DigitGenerator()
    excluded_digit = 9
    digit = generator.get_digit_excluding(excluded_digit)
    assert digit != excluded_digit  # Excluded digit is 9
    assert digit in range(10)  # Result is a valid digit key

def test_digit_generator_invalid_input_string():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_excluding("not_a_digit")
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"

def test_digit_generator_invalid_input_float():
    # Testing with a float as an invalid type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_excluding(3.14)
    assert "<class 'float'>" in str(excinfo.value)

def test_digit_generator_invalid_input_out_of_range_positive():
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_excluding(10)
    assert "<class 'int'>" in str(excinfo.value)

def test_digit_generator_invalid_input_out_of_range_negative():
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_excluding(-1)
    assert "<class 'int'>" in str(excinfo.value)