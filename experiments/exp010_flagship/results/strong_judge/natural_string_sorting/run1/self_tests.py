from solution import sort_strings_naturally

def test_sort_strings_naturally_ascending_default_order():
    # AC-1.1: Default order should be ascending
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]  # computed from specification
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_ascending_numeric_comparison():
    # AC-1.2: Numbers compare by numeric value rather than character order
    input_data = ["3", "23", "2", "1"]
    expected_output = ["1", "2", "3", "23"]  # computed from specification
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_ascending_digit_before_letter():
    # AC-1.3: Strings that begin with a digit precede strings that begin with a letter
    input_data = ["b1", "1", "a1"]
    expected_output = ["1", "a1", "b1"]  # computed from specification
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_ascending_canonical_example():
    # AC-1.4: Canonical worked example
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]  # computed from specification
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_descending_order():
    # AC-2.1: Descending order is the reverse of ascending order
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    ascending_result = sort_strings_naturally(input_data)
    expected_output = list(reversed(ascending_result))  # computed from specification
    assert sort_strings_naturally(input_data, descending=True) == expected_output

def test_sort_strings_naturally_descending_canonical_example():
    # AC-2.2: Canonical worked example for descending order
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    ascending_result = sort_strings_naturally(input_data)
    expected_output = list(reversed(ascending_result))  # computed from specification
    assert sort_strings_naturally(input_data, descending=True) == expected_output

def test_sort_strings_naturally_non_canonical_example():
    # General test to verify algorithm: natural ordering of mixed text
    input_data = ["file10", "file2", "file1"]
    expected_output = ["file1", "file2", "file10"]  # computed from specification
    assert sort_strings_naturally(input_data) == expected_output