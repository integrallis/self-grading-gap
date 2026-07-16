import pytest
from solution import read_term, iterate_term

def test_read_term():
    # AC-1.1
    assert read_term("1") == "11"          # one 1 -> "11"
    assert read_term("11") == "21"         # two 1s -> "21"
    assert read_term("21") == "1211"       # one 2, then one 1 -> "1211"
    assert read_term("1211") == "111221"   # one 1, one 2, then two 1s -> "111221"
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1 -> "312211"
    assert read_term("2") == "12"          # one 2 -> "12"
    assert read_term("3211") == "131221"   # one 3, one 2, two 1s -> "131221"
    
    # AC-1.2
    assert read_term("1111111111") == "101"  # ten 1s -> "101"
    assert read_term("11111111111") == "111"  # eleven 1s -> "111"

    # AC-1.3
    assert read_term("22") == "22"          # fixed point -> "22"
    
    # AC-1.4
    assert read_term("10") == "1110"        # one 1, one 0 -> "1110"
    assert read_term("9") == "19"           # one 9 -> "19"
    assert read_term("0123456789") == "10111213141516171819"  # one of each digit

def test_iterate_term():
    # AC-2.1
    assert iterate_term("1", 0) == "1"      # zero iterations -> "1"
    
    # AC-2.2
    assert iterate_term("1", 1) == "11"     # one step -> "11"
    assert iterate_term("1", 2) == "21"     # two steps -> "21"
    assert iterate_term("1", 5) == "312211"  # five steps -> "312211"
    assert iterate_term("2", 1) == "12"     # one step from "2" -> "12"
    
    # AC-2.3
    assert iterate_term("22", 3) == "22"    # three steps on a fixed point -> "22"

def test_input_validation():
    # AC-3.1
    with pytest.raises(Exception) as exc_info:
        iterate_term("1", -1)
    assert str(exc_info.value) == "iterations must be non-negative"
    
    # AC-3.2
    with pytest.raises(Exception) as exc_info:
        iterate_term("", 1)
    assert str(exc_info.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as exc_info:
        iterate_term("abc", 1)
    assert str(exc_info.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as exc_info:
        iterate_term("1a", 1)
    assert str(exc_info.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as exc_info:
        iterate_term("1.0", 1)
    assert str(exc_info.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as exc_info:
        iterate_term("A1", 1)
    assert str(exc_info.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as exc_info:
        read_term("A1")
    assert str(exc_info.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as exc_info:
        read_term("")
    assert str(exc_info.value) == "term must be a non-empty string of digits"