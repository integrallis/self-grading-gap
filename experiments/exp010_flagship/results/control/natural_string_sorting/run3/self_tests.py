from solution import sort_mixed_text

def test_sort_mixed_text_ascending_no_direction():
    # AC-1.1: Default is ascending order
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_ascending_digit_precedes_letter():
    # AC-1.3: Strings that begin with a digit precede strings that begin with a letter
    input_data = ["b2", "1a", "2b", "1", "a"]
    expected_output = ["1", "1a", "2b", "b2", "a"]  # "1" precedes "1a", and then "2b", "b2", "a"
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_ascending_numeric_value():
    # AC-1.2: Numbers embedded in strings compare by numeric value
    input_data = ["10", "2", "1", "12", "3"]
    expected_output = ["1", "2", "3", "10", "12"]  # Sorted by numeric value
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_descending():
    # AC-2.1: Descending order is the reverse of ascending order
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]  # Reversed order
    assert sort_mixed_text(input_data, descending=True) == expected_output