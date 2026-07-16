from solution import Calculator, DigitGenerator

def test_calculator_initial_display():
    # AC-1.1: A freshly created calculator displays zero.
    calculator = Calculator()
    assert calculator.display() == "0"

def test_calculator_digit_entry_non_zero_start():
    # AC-2.1: A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
    calculator = Calculator()
    calculator.press('1')
    calculator.press('2')
    calculator.press('3')
    assert calculator.display() == "123"

def test_calculator_digit_entry_zero_only():
    # AC-2.2: Pressing only the zero key, any number of times, displays a single zero.
    calculator = Calculator()
    calculator.press('0')
    calculator.press('0')
    assert calculator.display() == "0"

def test_calculator_digit_entry_leading_zero():
    # AC-2.3: A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5".
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

def test_digit_generator_exclude_valid_digit():
    # AC-3.1: Asking for a digit key other than a given one always yields a valid digit key and never the excluded one.
    generator = DigitGenerator()
    excluded_digit = '5'
    generated_digit = generator.get_digit(excluded=excluded_digit)
    assert generated_digit != excluded_digit and generated_digit in '0123456789'

def test_digit_generator_exclude_invalid_digit():
    # AC-3.2: Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type.
    generator = DigitGenerator()
    with pytest.raises(NotImplementedError) as excinfo:
        generator.get_digit(excluded='invalid_string')
    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"