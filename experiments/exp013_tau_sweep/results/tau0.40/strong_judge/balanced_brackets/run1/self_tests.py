from solution import is_balanced

def test_empty_string_is_balanced():
    # The empty string is balanced.
    assert is_balanced("") == True

def test_single_matched_pair_is_balanced():
    # A single matched pair "[]" is balanced.
    assert is_balanced("[]") == True

def test_multiple_matched_pairs_are_balanced():
    # Multiple pairs in sequence "[][]" are balanced.
    assert is_balanced("[][]") == True

def test_nested_pairs_are_balanced():
    # Pairs nested inside other pairs "[[]]" are balanced.
    assert is_balanced("[[]]") == True

def test_complex_nesting_is_balanced():
    # Nested and sequenced pairs "[[[][]]]" are balanced.
    assert is_balanced("[[[][]]]") == True

def test_large_nesting_depth_is_balanced():
    # Fifty openers followed by fifty closers are balanced.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_bracket_before_opener_is_unbalanced():
    # A closing bracket arriving before its opener "][" is unbalanced.
    assert is_balanced("][" ) == False

def test_extra_closing_bracket_is_unbalanced():
    # A closing bracket with no matching opener "]" is unbalanced.
    assert is_balanced("]") == False

def test_unmatched_opening_bracket_is_unbalanced():
    # An opening bracket left unmatched "[" is unbalanced.
    assert is_balanced("[") == False

def test_unmatched_opening_brackets_is_unbalanced():
    # Multiple unmatched opening brackets "[[" is unbalanced.
    assert is_balanced("[[") == False

def test_closing_bracket_with_no_opener_is_unbalanced():
    # Extra closing brackets with no matching opener "]]" is unbalanced.
    assert is_balanced("]]") == False

def test_extra_unmatched_brackets_after_valid_pairs_are_unbalanced():
    # Extra unmatched brackets after valid pairs "[][]][" is unbalanced.
    assert is_balanced("[][]][") == False

def test_closing_bracket_before_opener_in_mixed_is_unbalanced():
    # Another case where a closing bracket arrives before its opener "][][" is unbalanced.
    assert is_balanced("][][") == False

def test_unmatched_opening_brackets_with_nested_is_unbalanced():
    # Unmatched brackets with nested brackets "[[]" is unbalanced.
    assert is_balanced("[[]") == False

def test_closing_bracket_with_no_opener_in_pair_is_unbalanced():
    # Closing bracket with no matching opener in a pair "[]]" is unbalanced.
    assert is_balanced("[]]") == False