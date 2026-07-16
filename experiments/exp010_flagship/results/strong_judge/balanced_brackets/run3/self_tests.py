from solution import is_balanced

def test_empty_string_is_balanced():
    # The empty string is balanced.
    assert is_balanced("") == True

def test_single_matched_pair_is_balanced():
    # A single matched pair "[]" is balanced.
    assert is_balanced("[]") == True

def test_multiple_pairs_in_sequence_are_balanced():
    # Multiple pairs "[][]" are balanced.
    assert is_balanced("[][]") == True

def test_pairs_nested_inside_other_pairs_are_balanced():
    # Pairs nested "[[]]" are balanced.
    assert is_balanced("[[]]") == True

def test_mixed_nesting_and_sequencing_are_balanced():
    # Mixed nesting and sequencing "[[[][]]]" is balanced.
    assert is_balanced("[[[][]]]") == True

def test_large_nesting_depth_is_balanced():
    # Fifty openers followed by fifty closers are balanced.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_bracket_before_opener_makes_unbalanced():
    # A closing bracket arriving before its opener "][" makes unbalanced.
    assert is_balanced("][") == False

def test_closing_bracket_before_opener_in_sequence_is_unbalanced():
    # Closing bracket before its opener in sequence "[][[" is unbalanced.
    assert is_balanced("][][") == False

def test_opening_brackets_left_unmatched_are_unbalanced():
    # Opening brackets left unmatched "[" make unbalanced.
    assert is_balanced("[") == False

def test_multiple_opening_brackets_left_unmatched_are_unbalanced():
    # Multiple opening brackets left unmatched "[[" make unbalanced.
    assert is_balanced("[[") == False

def test_opening_brackets_with_nested_closing_are_unbalanced():
    # Opening brackets with unmatched closing "[[]" make unbalanced.
    assert is_balanced("[[]") == False

def test_closing_brackets_with_no_matching_opener_are_unbalanced():
    # Closing brackets with no matching opener "]" make unbalanced.
    assert is_balanced("]") == False

def test_multiple_closing_brackets_with_no_matching_opener_are_unbalanced():
    # Multiple closing brackets with no matching opener "]]" make unbalanced.
    assert is_balanced("]]") == False

def test_closing_bracket_after_valid_pairs_is_unbalanced():
    # Extra unmatched brackets after valid pairs "[][]][" make unbalanced.
    assert is_balanced("[][]]") == False