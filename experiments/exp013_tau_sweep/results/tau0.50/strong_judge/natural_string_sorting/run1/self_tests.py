from solution import sort_natural

def test_sort_natural_ascending_no_direction():
    # When no direction is requested, the collection is returned sorted in natural ascending order.
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]  # Canonical example
    assert sort_natural(input_data) == expected_output

def test_sort_natural_ascending_numbers():
    # Numbers embedded in strings compare by numeric value rather than by character order.
    input_data = ["3", "23", "2"]
    expected_output = ["2", "3", "23"]  # Numeric comparison
    assert sort_natural(input_data) == expected_output

def test_sort_natural_ascending_digit_first():
    # Strings that begin with a digit precede strings that begin with a letter.
    input_data = ["a1", "1", "b1", "2"]
    expected_output = ["1", "2", "a1", "b1"]  # Digit strings first
    assert sort_natural(input_data) == expected_output

def test_sort_natural_descending():
    # When descending order is requested, the result is the exact reverse of the natural ascending order.
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]  # Canonical reverse example
    assert sort_natural(input_data, descending=True) == expected_output  # Explicitly requesting descending order

def test_sort_natural_descending_equivalence():
    # Testing that explicitly requested descending output is the exact reverse of the ascending output
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = list(reversed(["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]))  # Reverse of ascending order
    assert sort_natural(input_data, descending=True) == expected_output  # Explicitly requesting descending order