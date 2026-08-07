# test_look_and_say.py

from solution import read_term, iterate_from_seed
import pytest

def test_read_term_single_digit():
    assert read_term("1") == "11"  # "1" becomes "11"
    assert read_term("2") == "12"  # "2" becomes "12"
    assert read_term("9") == "19"  # "9" becomes "19"
    
def test_read_term_multiple_identical_digits():
    assert read_term("11") == "21"  # "11" becomes "21"
    assert read_term("111") == "31"  # "111" becomes "31"
    assert read_term("1111") == "41"  # "1111" becomes "41"
    assert read_term("11111") == "51"  # "11111" becomes "51"
    
def test_read_term_various_runs():
    assert read_term("21") == "1211"  # "21" becomes "1211"
    assert read_term("1211") == "111221"  # "1211" becomes "111221"
    assert read_term("111221") == "312211"  # "111221" becomes "312211"
    assert read_term("3211") == "131221"  # "3211" becomes "131221"

def test_read_term_fixed_point():
    assert read_term("22") == "22"  # "22" reads as itself

def test_read_term_large_run():
    assert read_term("1111111111") == "101"  # ten 1s become "101"
    
def test_read_term_zero_and_ten():
    assert read_term("10") == "1110"  # "10" becomes "1110"
    
def test_iterate_from_seed_zero_iterations():
    assert iterate_from_seed("1", 0) == "1"  # Zero iterations return the seed unchanged
    assert iterate_from_seed("2", 0) == "2"  # Zero iterations return the seed unchanged
    
def test_iterate_from_seed_multiple_iterations():
    assert iterate_from_seed("1", 1) == "11"  # One step gives "11"
    assert iterate_from_seed("1", 2) == "21"  # Two steps give "21"
    assert iterate_from_seed("1", 5) == "312211"  # Five steps give "312211"
    assert iterate_from_seed("2", 1) == "12"  # One step from "2" gives "12"
    
def test_iterate_from_seed_fixed_point():
    assert iterate_from_seed("22", 3) == "22"  # "22" is still "22" after three steps

def test_invalid_term_empty():
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        read_term("")
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        iterate_from_seed("", 1)

def test_invalid_term_non_digit_characters():
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        read_term("a")
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        read_term("1a")
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        iterate_from_seed("1A", 1)
    with pytest.raises(Exception, match=r"\Aterm must be a non-empty string of digits\Z"):
        iterate_from_seed("1!", 1)

def test_invalid_iterations_negative():
    with pytest.raises(Exception, match=r"\Aiterations must be non-negative\Z"):
        iterate_from_seed("1", -1)