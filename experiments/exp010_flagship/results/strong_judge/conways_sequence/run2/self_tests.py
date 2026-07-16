from solution import read_term, iterate_from_seed
import pytest

def test_read_term_single_digit():
    assert read_term("1") == "11"  # "1" becomes "11"
    assert read_term("2") == "12"  # "2" becomes "12"
    assert read_term("3") == "13"  # "3" becomes "13"
    assert read_term("0") == "10"  # "0" becomes "10"
    assert read_term("9") == "19"  # "9" becomes "19"

def test_read_term_multiple_identical_digits():
    assert read_term("11") == "21"  # "11" becomes "21"
    assert read_term("22") == "22"  # "22" reads as itself
    assert read_term("111") == "31"  # "111" becomes "31"
    assert read_term("1111") == "41"  # "1111" becomes "41"
    assert read_term("22222") == "52"  # "22222" becomes "52"
    assert read_term("00000") == "50"  # "00000" becomes "50"

def test_read_term_varied_runs():
    assert read_term("3211") == "131221"  # "3211" becomes "131221"
    assert read_term("1211") == "111221"  # "1211" becomes "111221"
    assert read_term("111221") == "312211"  # "111221" becomes "312211"
    assert read_term("21") == "1211"  # "21" becomes "1211"

def test_read_term_ten_or_more_identical_digits():
    assert read_term("1111111111") == "101"  # ten 1s become "101"
    assert read_term("0000000000") == "100"  # ten 0s become "100"
    assert read_term("11111111111") == "111"  # eleven 1s become "111"

def test_read_term_mixed_digits():
    assert read_term("10") == "1110"  # "10" becomes "1110"

def test_iterate_from_seed_zero_iterations():
    assert iterate_from_seed("1", 0) == "1"  # zero iterations return the seed unchanged
    assert iterate_from_seed("2", 0) == "2"  # zero iterations return the seed unchanged
    assert iterate_from_seed("22", 0) == "22"  # zero iterations return the seed unchanged
    with pytest.raises(Exception) as caught_exception:
        iterate_from_seed("", 0)  # empty term should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"

def test_iterate_from_seed_multiple_iterations():
    assert iterate_from_seed("1", 1) == "11"  # 1 step from "1" gives "11"
    assert iterate_from_seed("1", 2) == "21"  # 2 steps from "1" gives "21"
    assert iterate_from_seed("1", 5) == "312211"  # 5 steps from "1" gives "312211"
    assert iterate_from_seed("2", 1) == "12"  # 1 step from "2" gives "12"
    assert iterate_from_seed("22", 3) == "22"  # 3 steps from "22" still gives "22"

def test_iterate_from_seed_invalid_iterations():
    with pytest.raises(Exception) as caught_exception:
        iterate_from_seed("1", -1)  # negative iteration count should raise an error
    assert str(caught_exception.value) == "iterations must be non-negative"

def test_iterate_from_seed_invalid_term():
    with pytest.raises(Exception) as caught_exception:
        iterate_from_seed("", 1)  # empty term should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"
    
    with pytest.raises(Exception) as caught_exception:
        iterate_from_seed("1a", 1)  # term with non-digit should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"
    
    with pytest.raises(Exception) as caught_exception:
        iterate_from_seed("1.5", 1)  # term with non-digit should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"
    
    with pytest.raises(Exception) as caught_exception:
        iterate_from_seed("1A", 1)  # term with uppercase letter should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"

def test_read_term_invalid_terms():
    with pytest.raises(Exception) as caught_exception:
        read_term("")  # empty term should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"
    
    with pytest.raises(Exception) as caught_exception:
        read_term("1a")  # term with non-digit should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"
    
    with pytest.raises(Exception) as caught_exception:
        read_term("1.5")  # term with non-digit should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"
    
    with pytest.raises(Exception) as caught_exception:
        read_term("1A")  # term with uppercase letter should raise an error
    assert str(caught_exception.value) == "term must be a non-empty string of digits"