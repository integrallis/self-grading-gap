from solution import is_balanced

def test_empty_string():
    # The empty string is balanced.
    assert is_balanced("") == True

def test_single_matched_pair():
    # A single matched pair is balanced.
    assert is_balanced("[]") == True

def test_multiple_matched_pairs():
    # Multiple pairs in sequence are balanced.
    assert is_balanced("[][]") == True

def test_nested_pairs():
    # Pairs nested inside other pairs are balanced.
    assert is_balanced("[[]]") == True
    assert is_balanced("[[[][]]]") == True

def test_large_nesting():
    # Nesting depth is not limited by a small bound: fifty openers followed by fifty closers are balanced.
    assert is_balanced("[" * 50 + "]" * 50) == True

def test_closing_before_opener():
    # A closing bracket arriving before its opener makes the string unbalanced.
    assert is_balanced("][" ) == False
    assert is_balanced("][][" ) == False

def test_unmatched_opening_brackets():
    # Opening brackets left unmatched make the string unbalanced.
    assert is_balanced("[") == False
    assert is_balanced("[[") == False
    assert is_balanced("[[]") == False

def test_unmatched_closing_brackets():
    # Closing brackets with no matching opener make the string unbalanced.
    assert is_balanced("]") == False
    assert is_balanced("]]") == False
    assert is_balanced("[]]") == False

def test_extra_unmatched_brackets():
    # Extra unmatched brackets after otherwise valid pairs make the string unbalanced.
    assert is_balanced("[][]]") == False