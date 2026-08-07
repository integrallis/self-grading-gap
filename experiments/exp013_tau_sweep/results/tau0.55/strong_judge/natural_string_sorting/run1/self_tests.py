from solution import natural_sort

def test_natural_sort_ascending_no_direction():
    # Expected: ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    result = natural_sort(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"])
    expected = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert result == expected

def test_natural_sort_ascending_numerical_comparison():
    # Expected: ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    result = natural_sort(["3", "23", "1", "2", "0", "1a", "a1", "b1", "b3", "z 21", "21 1", "z22"])
    expected = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert result == expected

def test_natural_sort_ascending_strings_starting_with_digit():
    # Expected: ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    result = natural_sort(["1", "a1", "3", "b1", "2", "1a", "b3", "23", "z 21", "21 1", "z22", "0"])
    expected = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]
    assert result == expected

def test_natural_sort_descending_order():
    # Expected: ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    result = natural_sort(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"], descending=True)
    expected = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    assert result == expected

def test_natural_sort_descending_reverse_of_ascending():
    # Expected: ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]
    ascending_result = natural_sort(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"])
    descending_result = natural_sort(["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"], descending=True)
    assert descending_result == ascending_result[::-1]

def test_natural_sort_non_canonical_ascending():
    # Expected: ["item1", "item2", "item10"]
    result = natural_sort(["item10", "item2", "item1"])
    expected = ["item1", "item2", "item10"]
    assert result == expected