from solution import sort_naturally

def test_sort_naturally_ascending_default():
    # "a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"
    # sorts ascending to:
    expected = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    result = sort_naturally(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"])
    assert result == expected

def test_sort_naturally_ascending_with_numerics():
    # "10", "2", "1", "20"
    # sorts ascending to:
    expected = ["1", "2", "10", "20"]
    result = sort_naturally(["10", "2", "1", "20"])
    assert result == expected

def test_sort_naturally_ascending_with_leading_digits():
    # "apple", "2banana", "banana", "1apple"
    # sorts ascending to:
    expected = ["1apple", "2banana", "banana", "apple"]
    result = sort_naturally(["apple", "2banana", "banana", "1apple"])
    assert result == expected

def test_sort_naturally_descending():
    # "a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"
    # sorts descending to:
    expected = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    result = sort_naturally(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"], reverse=True)
    assert result == expected

def test_sort_naturally_descending_with_numerics():
    # "10", "2", "1", "20"
    # sorts descending to:
    expected = ["20", "10", "2", "1"]
    result = sort_naturally(["10", "2", "1", "20"], reverse=True)
    assert result == expected

def test_sort_naturally_descending_with_leading_digits():
    # "apple", "2banana", "banana", "1apple"
    # sorts descending to:
    expected = ["banana", "apple", "2banana", "1apple"]
    result = sort_naturally(["apple", "2banana", "banana", "1apple"], reverse=True)
    assert result == expected