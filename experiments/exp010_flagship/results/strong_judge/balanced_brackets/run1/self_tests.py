from solution import is_balanced

def test_empty_string_is_balanced():
    # The empty string has no brackets, thus it is balanced.
    assert is_balanced("") == True

def test_single_matched_pair_is_balanced():
    # The string "[]" contains one matched pair, so it is balanced.
    assert is_balanced("[]") == True

def test_multiple_pairs_in_sequence_are_balanced():
    # The string "[][]" contains two matched pairs in sequence, so it is balanced.
    assert is_balanced("[][]") == True

def test_nested_pairs_are_balanced():
    # The string "[[]]" contains nested matched pairs, so it is balanced.
    assert is_balanced("[[]]") == True

def test_mixed_nesting_and_sequencing_are_balanced():
    # The string "[[[][]]]" contains nested and sequenced matched pairs, so it is balanced.
    assert is_balanced("[[[][]]]") == True

def test_large_nesting_depth_is_balanced():
    # The string with fifty openers followed by fifty closers is balanced.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_before_opener_makes_unbalanced():
    # The string "][" has a closing bracket before its opener, so it is unbalanced.
    assert is_balanced("][" ) == False

def test_unmatched_opening_brackets_make_unbalanced():
    # The string "[" has an unmatched opening bracket, so it is unbalanced.
    assert is_balanced("[") == False

def test_multiple_unmatched_opening_brackets_make_unbalanced():
    # The string "[[" has multiple unmatched opening brackets, so it is unbalanced.
    assert is_balanced("[[") == False

def test_nested_unmatched_opening_brackets_make_unbalanced():
    # The string "[[]" has an unmatched opening bracket, so it is unbalanced.
    assert is_balanced("[[]") == False

def test_closing_without_opener_is_unbalanced():
    # The string "]" has a closing bracket with no matching opener, so it is unbalanced.
    assert is_balanced("]") == False

def test_multiple_closing_without_opener_is_unbalanced():
    # The string "]]" has multiple closing brackets with no matching opener, so it is unbalanced.
    assert is_balanced("]]") == False

def test_closing_bracket_after_valid_pairs_is_unbalanced():
    # The string "[][]]" has an extra unmatched closing bracket after valid pairs, so it is unbalanced.
    assert is_balanced("[][]]") == False