# your complete test file
from solution import natural_sort

def test_natural_sort_ascending_no_direction():
    # AC-1.1: No direction requested, should sort in natural ascending order
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]  # Computed from specification
    assert natural_sort(input_data) == expected_output

def test_natural_sort_ascending_numbers_before_letters():
    # AC-1.3: Strings that begin with a digit precede strings that begin with a letter
    input_data = ["apple", "1banana", "2apple", "banana1"]
    expected_output = ["1banana", "2apple", "apple", "banana1"]  # Computed from specification
    assert natural_sort(input_data) == expected_output

def test_natural_sort_ascending_numbers_compared_by_value():
    # AC-1.2: Numbers embedded in strings compare by numeric value
    input_data = ["item2", "item10", "item1"]
    expected_output = ["item1", "item2", "item10"]  # Computed from specification
    assert natural_sort(input_data) == expected_output

def test_natural_sort_descending_order():
    # AC-2.1: When descending order is requested, the result is the reverse of ascending
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]  # Computed from specification
    assert natural_sort(input_data, direction='descending') == expected_output

def test_natural_sort_descending_numbers_before_letters():
    # AC-2.1: When descending order is requested, the result is the reverse of ascending
    input_data = ["apple", "1banana", "2apple", "banana1"]
    expected_output = ["banana1", "apple", "2apple", "1banana"]  # Computed from specification
    assert natural_sort(input_data, direction='descending') == expected_output

def test_natural_sort_descending_numbers_compared_by_value():
    # AC-2.1: When descending order is requested, the result is the reverse of ascending
    input_data = ["item2", "item10", "item1"]
    expected_output = ["item10", "item2", "item1"]  # Computed from specification
    assert natural_sort(input_data, direction='descending') == expected_output