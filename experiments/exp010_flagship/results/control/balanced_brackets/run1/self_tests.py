from solution import is_balanced

def test_empty_string():
    # The empty string is balanced.
    assert is_balanced("") == True

def test_single_matched_pair():
    # A single matched pair "[]" is balanced.
    assert is_balanced("[]") == True

def test_multiple_pairs_in_sequence():
    # Multiple pairs in sequence "[][]" are balanced.
    assert is_balanced("[][]") == True

def test_nested_pairs():
    # Pairs nested inside other pairs "[[]]" are balanced.
    assert is_balanced("[[]]") == True

def test_nested_and_sequenced_pairs():
    # Mixed nesting and sequencing "[[[][]]]" is balanced.
    assert is_balanced("[[[][]]]") == True

def test_deep_nesting():
    # Fifty openers followed by fifty closers are balanced.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_bracket_before_opener():
    # A closing bracket arriving before its opener "][" makes the string unbalanced.
    assert is_balanced("][") == False

def test_unmatched_opening_bracket():
    # An opening bracket left unmatched "[" makes the string unbalanced.
    assert is_balanced("[") == False

def test_closing_bracket_with_no_matching_opener():
    # A closing bracket with no matching opener "]" makes the string unbalanced.
    assert is_balanced("]") == False

def test_extra_unmatched_brackets():
    # Extra unmatched brackets after otherwise valid pairs "[][]][" make the string unbalanced.
    assert is_balanced("[][]][") == False

def test_unmatched_opening_brackets():
    # Multiple unmatched opening brackets "[[" make the string unbalanced.
    assert is_balanced("[[") == False

def test_unmatched_closing_brackets():
    # Multiple unmatched closing brackets "]]" make the string unbalanced.
    assert is_balanced("]]") == False

def test_closing_bracket_with_no_matching_opener_multiple():
    # Closing brackets with no matching opener "[]]" make the string unbalanced.
    assert is_balanced("[]]") == False