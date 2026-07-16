from solution import is_balanced

def test_empty_string_is_balanced():
    # The empty string is balanced.
    assert is_balanced("") == True

def test_single_matched_pair_is_balanced():
    # A single matched pair "[]" is balanced.
    assert is_balanced("[]") == True

def test_multiple_pairs_in_sequence_are_balanced():
    # Multiple pairs in sequence "[][]" are balanced.
    assert is_balanced("[][]") == True

def test_nested_pairs_are_balanced():
    # Pairs nested inside other pairs "[[]]" are balanced.
    assert is_balanced("[[]]") == True

def test_mixed_nesting_and_sequencing_are_balanced():
    # Mixed nesting and sequencing "[[[][]]]" are balanced.
    assert is_balanced("[[[][]]]") == True

def test_large_nesting_depth_is_balanced():
    # Fifty openers followed by fifty closers are balanced.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_bracket_before_opener_is_unbalanced():
    # A closing bracket arriving before its opener "][" makes the string unbalanced.
    assert is_balanced("][" ) == False

def test_opening_brackets_left_unmatched_is_unbalanced():
    # Opening brackets left unmatched "[[" makes the string unbalanced.
    assert is_balanced("[[") == False

def test_closing_brackets_with_no_matching_opener_is_unbalanced():
    # Closing brackets with no matching opener "]" makes the string unbalanced.
    assert is_balanced("]") == False

def test_extra_unmatched_brackets_after_valid_pairs_is_unbalanced():
    # Extra unmatched brackets after otherwise valid pairs "[][]][" makes the string unbalanced.
    assert is_balanced("[][]][") == False