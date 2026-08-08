from solution import is_balanced

def test_empty_string():
    assert is_balanced("")  # The empty string is balanced.

def test_single_matched_pair():
    assert is_balanced("[]")  # A single matched pair is balanced.

def test_multiple_pairs_in_sequence():
    assert is_balanced("[][]")  # Multiple pairs in sequence are balanced.

def test_nested_pairs():
    assert is_balanced("[[]]")  # Pairs nested inside other pairs are balanced.

def test_complex_nesting():
    assert is_balanced("[[[][]]]")  # Complex nesting of pairs is balanced.

def test_large_balanced_string():
    assert is_balanced("[" * 50 + "]" * 50)  # Fifty openers followed by fifty closers are balanced.

def test_closing_before_opening():
    assert not is_balanced("][" )  # A closing bracket arrives before its opener makes it unbalanced.

def test_extra_closing_brackets():
    assert not is_balanced("][][")  # A closing bracket arrives before its opener makes it unbalanced.

def test_opening_brackets_left_unmatched():
    assert not is_balanced("[")  # An opening bracket left unmatched makes it unbalanced.
    assert not is_balanced("[[")  # Multiple opening brackets left unmatched makes it unbalanced.
    assert not is_balanced("[[]")  # An opening bracket left unmatched makes it unbalanced.

def test_closing_brackets_with_no_matching_opener():
    assert not is_balanced("]")  # Closing brackets with no matching opener make it unbalanced.
    assert not is_balanced("]]")  # Extra closing brackets with no matching opener make it unbalanced.
    assert not is_balanced("[]]")  # A closing bracket with no matching opener makes it unbalanced.

def test_extra_unmatched_brackets():
    assert not is_balanced("[][]][")  # Extra unmatched brackets after otherwise valid pairs make it unbalanced.