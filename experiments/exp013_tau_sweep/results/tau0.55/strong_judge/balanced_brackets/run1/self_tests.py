from solution import is_balanced

def test_empty_string():
    # The empty string is balanced.
    assert is_balanced("") is True

def test_single_matched_pair():
    # A single matched pair "[]" is balanced.
    assert is_balanced("[]") is True

def test_multiple_pairs_in_sequence():
    # Multiple pairs in sequence "[][]" are balanced.
    assert is_balanced("[][]") is True

def test_nested_pairs():
    # Pairs nested inside other pairs "[[]]" are balanced.
    assert is_balanced("[[]]") is True

def test_mixed_nesting_and_sequencing():
    # Mixed nesting and sequencing "[[[][]]]" is balanced.
    assert is_balanced("[[[][]]]") is True

def test_large_balance():
    # Fifty openers followed by fifty closers are balanced.
    assert is_balanced("[" * 50 + "]" * 50) is True

def test_closing_before_opener():
    # A closing bracket arriving before its opener "][" is unbalanced.
    assert is_balanced("][" ) is False

def test_unmatched_opening_brackets():
    # Opening brackets left unmatched "[", "[[", "[[]".
    assert is_balanced("[") is False
    assert is_balanced("[[") is False
    assert is_balanced("[[]") is False

def test_closing_without_opener():
    # Closing brackets with no matching opener "]", "]]", "[]]".
    assert is_balanced("]") is False
    assert is_balanced("]]") is False
    assert is_balanced("[]]") is False

def test_extra_unmatched_brackets():
    # Extra unmatched brackets after otherwise valid pairs "[][]]["
    assert is_balanced("[][]][") is False