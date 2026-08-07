from solution import sort_mixed_text

def test_sort_mixed_text_ascending_default():
    # Example: "a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_ascending_no_direction():
    # Example: "10", "2", "1", "20", "3"
    input_data = ["10", "2", "1", "20", "3"]
    expected_output = ["1", "2", "3", "10", "20"]  # Numeric ordering
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_ascending_with_letters():
    # Example: "a10", "a2", "a1", "b20", "b3"
    input_data = ["a10", "a2", "a1", "b20", "b3"]
    expected_output = ["a1", "a2", "b3", "a10", "b20"]  # Letters after numbers
    assert sort_mixed_text(input_data) == expected_output

def test_sort_mixed_text_descending():
    # Example: "a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"
    input_data = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    expected_output = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]  # Reverse of ascending order
    assert sort_mixed_text(input_data, descending=True) == expected_output

def test_sort_mixed_text_descending_no_direction():
    # Example: "10", "2", "1", "20", "3"
    input_data = ["10", "2", "1", "20", "3"]
    expected_output = ["20", "10", "3", "2", "1"]  # Reverse of ascending order
    assert sort_mixed_text(input_data, descending=True) == expected_output

def test_sort_mixed_text_descending_with_letters():
    # Example: "a10", "a2", "a1", "b20", "b3"
    input_data = ["a10", "a2", "a1", "b20", "b3"]
    expected_output = ["b20", "a10", "b3", "a2", "a1"]  # Reverse of ascending order
    assert sort_mixed_text(input_data, descending=True) == expected_output