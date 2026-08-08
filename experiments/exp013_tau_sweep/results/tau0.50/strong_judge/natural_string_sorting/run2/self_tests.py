from solution import sort_strings_naturally

def test_sort_strings_naturally_ascending_default():
    # Expected: "0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_ascending_with_numbers():
    # Expected: "0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"
    input_data = ["3", "2", "1", "1a", "0"]
    expected_output = ["0", "1", "1a", "2", "3"]
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_ascending_with_letters():
    # Expected: "a1", "b1", "b3", "z 21", "z22"
    input_data = ["b3", "a1", "b1", "z22", "z 21"]
    expected_output = ["a1", "b1", "b3", "z 21", "z22"]
    assert sort_strings_naturally(input_data) == expected_output

def test_sort_strings_naturally_descending():
    # Expected: "z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    assert sort_strings_naturally(input_data, descending=True) == expected_output

def test_sort_strings_naturally_descending_with_numbers():
    # Expected: "3", "2", "1", "1a", "0"
    input_data = ["0", "1", "1a", "2", "3"]
    expected_output = ["3", "2", "1", "1a", "0"]
    assert sort_strings_naturally(input_data, descending=True) == expected_output

def test_sort_strings_naturally_descending_with_letters():
    # Expected: "z22", "z 21", "b3", "b1", "a1"
    input_data = ["b1", "a1", "b3", "z22", "z 21"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1"]
    assert sort_strings_naturally(input_data, descending=True) == expected_output