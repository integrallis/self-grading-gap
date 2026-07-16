# test_calculator.py

from solution import Calculator, DigitKeyGenerator

def test_switch_on_state():
    # A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

def test_digit_entry_non_zero_start():
    # A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press_digit('2')  # first press
    calculator.press_digit('5')  # second press
    assert calculator.display() == "25"  # expected value is "25"

def test_digit_entry_only_zeros():
    # Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    calculator.press_digit('0')  # first press
    calculator.press_digit('0')  # second press
    assert calculator.display() == "0"  # expected value is "0"

def test_digit_entry_leading_zero_replacement():
    # A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
    calculator = Calculator()
    calculator.press_digit('0')  # first press
    calculator.press_digit('5')  # second press
    assert calculator.display() == "5"  # expected value is "5"

def test_digit_entry_significant_zeros():
    # Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".
    calculator = Calculator()
    calculator.press_digit('1')  # first press
    calculator.press_digit('0')  # second press
    calculator.press_digit('5')  # third press
    assert calculator.display() == "105"  # expected value is "105"

def test_digit_key_generator_exclude():
    # Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitKeyGenerator()
    excluded_key = '3'
    for _ in range(100):  # test multiple times to ensure randomness
        key = generator.get_digit_key(excluded=excluded_key)
        assert key != excluded_key  # expected that key is not the excluded one
        assert key in '0123456789'  # expected that key is a valid digit

def test_digit_key_generator_invalid_type():
    # Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitKeyGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit_key(excluded='invalid')  # passing a string
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"  # expected error message