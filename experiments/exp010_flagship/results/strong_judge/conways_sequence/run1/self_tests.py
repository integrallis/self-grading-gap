import pytest
from solution import read_term, iterate_from_seed

def test_read_term():
    # AC-1.1: "1" becomes "11"
    assert read_term("1") == "11"  # one 1
    # AC-1.1: "11" becomes "21"
    assert read_term("11") == "21"  # two 1s
    # AC-1.1: "21" becomes "1211"
    assert read_term("21") == "1211"  # one 2, one 1
    # AC-1.1: "1211" becomes "111221"
    assert read_term("1211") == "111221"  # one 1, one 2, two 1s
    # AC-1.1: "111221" becomes "312211"
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1
    # AC-1.1: "2" becomes "12"
    assert read_term("2") == "12"  # one 2
    # AC-1.1: "3211" becomes "131221"
    assert read_term("3211") == "131221"  # one 3, one 2, two 1s
    # AC-1.2: Ten 1s become "101"
    assert read_term("1111111111") == "101"  # ten 1s
    # AC-1.3: "22" reads as itself
    assert read_term("22") == "22"  # two 2s, fixed point
    # AC-1.4: "10" becomes "1110"
    assert read_term("10") == "1110"  # one 1, one 0
    # AC-1.4: "9" becomes "19"
    assert read_term("9") == "19"  # one 9
    # AC-1.2: A run longer than ten digits
    assert read_term("111111111111") == "121"  # twelve 1s

def test_iterate_from_seed():
    # AC-2.1: Zero iterations return the seed unchanged
    assert iterate_from_seed("1", 0) == "1"
    # AC-2.2: One step from "1" gives "11"
    assert iterate_from_seed("1", 1) == "11"
    # AC-2.2: Two steps from "1" give "21"
    assert iterate_from_seed("1", 2) == "21"
    # AC-2.2: Five steps from "1" give "312211"
    assert iterate_from_seed("1", 5) == "312211"
    # AC-2.2: One step from "2" gives "12"
    assert iterate_from_seed("2", 1) == "12"
    # AC-2.3: Fixed point "22" after three steps still "22"
    assert iterate_from_seed("22", 3) == "22"

def test_input_validation():
    # AC-3.1: Negative iteration count is rejected
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1", -1)
    assert str(exc.value) == "iterations must be non-negative"
    
    # AC-3.2: Empty term is rejected
    with pytest.raises(Exception) as exc:
        iterate_from_seed("", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    
    # AC-3.2: Term with non-digit character is rejected
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1a", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    
    # AC-3.2: Term with upper-case letters is rejected
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1A", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    
    # AC-3.2: Term with lower-case letters is rejected
    with pytest.raises(Exception) as exc:
        iterate_from_seed("abc", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    
    # AC-3.2: Term with non-letter non-digit character is rejected
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1!", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"