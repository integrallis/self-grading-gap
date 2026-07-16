from solution import sort_natural

def test_sort_natural_ascending_no_direction():
    # Input: ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    # Expected output: ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert sort_natural(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]) == \
           ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]

def test_sort_natural_ascending_numbers_before_letters():
    # Input: ["3", "23", "1", "a", "2", "b"]
    # Expected output: ["1", "2", "3", "23", "a", "b"]
    assert sort_natural(["3", "23", "1", "a", "2", "b"]) == ["1", "2", "3", "23", "a", "b"]

def test_sort_natural_ascending_numbers_compare_by_value():
    # Input: ["10", "2", "1", "3"]
    # Expected output: ["1", "2", "3", "10"]
    assert sort_natural(["10", "2", "1", "3"]) == ["1", "2", "3", "10"]

def test_sort_natural_descending():
    # Input: ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    # Expected output: ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    assert sort_natural(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"], descending=True) == \
           ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]

def test_sort_natural_descending_numbers_before_letters():
    # Input: ["3", "23", "1", "a", "2", "b"]
    # Expected output: ["b", "a", "23", "3", "2", "1"]
    assert sort_natural(["3", "23", "1", "a", "2", "b"], descending=True) == ["b", "a", "23", "3", "2", "1"]

def test_sort_natural_descending_numbers_compare_by_value():
    # Input: ["10", "2", "1", "3"]
    # Expected output: ["10", "3", "2", "1"]
    assert sort_natural(["10", "2", "1", "3"], descending=True) == ["10", "3", "2", "1"]