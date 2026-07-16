from solution import sort_mixed_text

def test_sort_mixed_text_default_order():
    # AC-1.1: When no direction is requested, the collection is returned sorted in natural ascending order.
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_numerical_order():
    # AC-1.2: Numbers embedded in strings compare by numeric value rather than by character order.
    input_data = ["3", "23", "2", "1"]
    expected_output = ["1", "2", "3", "23"]  # numeric order
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_digit_before_letter():
    # AC-1.3: Strings that begin with a digit precede strings that begin with a letter.
    input_data = ["a1", "1", "b1", "2"]
    expected_output = ["1", "2", "a1", "b1"]  # digits before letters
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_canonical_example():
    # AC-1.4: Canonical worked example
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_descending_order():
    # AC-2.1: When descending order is requested, the result is the exact reverse of the natural ascending order.
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    assert sort_mixed_text(input_data, descending=True) == expected_output

def test_sort_mixed_text_descending_canonical_example():
    # AC-2.2: Canonical worked example for descending order
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    assert sort_mixed_text(input_data, descending=True) == expected_output