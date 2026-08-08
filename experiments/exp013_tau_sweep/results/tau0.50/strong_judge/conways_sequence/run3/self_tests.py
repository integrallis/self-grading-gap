import pytest
from solution import read_term, iterate

def test_read_term():
    # AC-1.1
    assert read_term("1") == "11"      # one 1
    assert read_term("11") == "21"     # two 1s
    assert read_term("21") == "1211"   # one 2, then one 1
    assert read_term("1211") == "111221" # one 1, one 2, two 1s
    assert read_term("111221") == "312211" # three 1s, two 2s, one 1
    assert read_term("2") == "12"      # one 2
    assert read_term("3211") == "131221" # one 3, one 2, two 1s
    
    # AC-1.2
    assert read_term("1111111111") == "101"  # ten 1s
    assert read_term("11111111111") == "111"  # eleven 1s
    
    # AC-1.3
    assert read_term("22") == "22"      # fixed point
    
    # AC-1.4
    assert read_term("10") == "1110"    # one 1, one 0
    assert read_term("9") == "19"       # one 9

def test_iterate():
    # AC-2.1
    assert iterate("1", 0) == "1"       # zero iterations
    
    # AC-2.2
    assert iterate("1", 1) == "11"      # one step
    assert iterate("1", 2) == "21"      # two steps
    assert iterate("1", 5) == "312211"   # five steps
    assert iterate("2", 1) == "12"      # one step from 2
    
    # AC-2.3
    assert iterate("22", 3) == "22"     # fixed point survives
    
def test_input_validation():
    # AC-3.1
    with pytest.raises(Exception, match=r"\Aiterations must be non-negative\Z"):
        iterate("1", -1)  # negative iteration count
    
    # AC-3.2
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        read_term("")    # empty term
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        read_term("1A")  # term with non-digit character
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        iterate("1A", 1)  # term with non-digit character in iterate
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        iterate("", 1)    # empty term in iterate
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        read_term("1.1")  # term with non-digit character