# test_bracket_balance.py

from solution import is_balanced

def test_empty_string_is_balanced():
    # An empty string has no unmatched brackets, hence it is balanced.
    assert is_balanced("") == True

def test_single_matched_pair_is_balanced():
    # A single pair "[]" is balanced as both opening and closing brackets match.
    assert is_balanced("[]") == True

def test_multiple_pairs_in_sequence_are_balanced():
    # Multiple pairs "[][]" are balanced as all opening and closing brackets match.
    assert is_balanced("[][]") == True

def test_nested_pairs_are_balanced():
    # Nested pairs "[[]]" are balanced as all opening and closing brackets match.
    assert is_balanced("[[]]") == True

def test_complex_nesting_and_sequencing_are_balanced():
    # Mixed nesting and sequencing "[[[][]]]" is balanced as all brackets match correctly.
    assert is_balanced("[[[][]]]") == True

def test_large_nesting_is_balanced():
    # Fifty openers followed by fifty closers are balanced as all brackets match.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_bracket_before_opener_is_unbalanced():
    # A closing bracket that comes before its opener "][" is unbalanced.
    assert is_balanced("][" ) == False

def test_closing_bracket_before_opener_in_sequence_is_unbalanced():
    # A sequence where a closing bracket comes before its opener "][]["
    assert is_balanced("][][") == False

def test_opening_brackets_left_unmatched_is_unbalanced():
    # An opening bracket left unmatched "[" is unbalanced.
    assert is_balanced("[") == False

def test_multiple_opening_brackets_left_unmatched_is_unbalanced():
    # Multiple opening brackets left unmatched "[[" is unbalanced.
    assert is_balanced("[[") == False

def test_nested_opening_brackets_left_unmatched_is_unbalanced():
    # A nested structure with unmatched opening brackets "[[]"
    assert is_balanced("[[]") == False

def test_closing_bracket_with_no_matching_opener_is_unbalanced():
    # A closing bracket with no matching opener "]" is unbalanced.
    assert is_balanced("]") == False

def test_multiple_closing_brackets_with_no_matching_opener_is_unbalanced():
    # Multiple closing brackets with no matching opener "]]" is unbalanced.
    assert is_balanced("]]") == False

def test_closing_bracket_after_valid_pairs_is_unbalanced():
    # Extra unmatched closing brackets after valid pairs "[][]]" is unbalanced.
    assert is_balanced("[][]]") == False

def test_extra_unmatched_brackets_is_unbalanced():
    # A sequence with extra unmatched closing brackets "[][]][" is unbalanced.
    assert is_balanced("[][]][") == False