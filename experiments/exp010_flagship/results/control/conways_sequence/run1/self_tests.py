# test_look_and_say.py

from solution import read_term, iterate_term

def test_read_term_single_digit():
    assert read_term("1") == "11"  # one 1 -> "11"
    assert read_term("2") == "12"  # one 2 -> "12"
    assert read_term("3") == "13"  # one 3 -> "13"
    assert read_term("0") == "10"  # one 0 -> "10"
    assert read_term("9") == "19"  # one 9 -> "19"

def test_read_term_multiple_identical_digits():
    assert read_term("11") == "21"  # two 1s -> "21"
    assert read_term("22") == "22"  # fixed point, unchanged
    assert read_term("111") == "31"  # three 1s -> "31"
    assert read_term("222") == "32"  # three 2s -> "32"
    assert read_term("00000") == "50"  # five 0s -> "50"
    assert read_term("000") == "30"  # three 0s -> "30"

def test_read_term_various_runs():
    assert read_term("21") == "1211"  # one 2, one 1 -> "1211"
    assert read_term("1211") == "111221"  # one 1, one 2, two 1s -> "111221"
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1 -> "312211"
    assert read_term("3211") == "131221"  # one 3, two 2s, one 1 -> "131221"

def test_read_term_large_runs():
    assert read_term("1111111111") == "101"  # ten 1s -> "101"

def test_iterate_term_zero_iterations():
    assert iterate_term("1", 0) == "1"  # zero iterations -> "1"
    assert iterate_term("2", 0) == "2"  # zero iterations -> "2"

def test_iterate_term_positive_iterations():
    assert iterate_term("1", 1) == "11"  # one step from "1" -> "11"
    assert iterate_term("1", 2) == "21"  # two steps from "1" -> "21"
    assert iterate_term("1", 5) == "312211"  # five steps from "1" -> "312211"
    assert iterate_term("2", 1) == "12"  # one step from "2" -> "12"
    assert iterate_term("22", 3) == "22"  # three steps from "22" -> "22"

def test_iterate_term_fixed_point():
    assert iterate_term("22", 1) == "22"  # still "22" after one step
    assert iterate_term("22", 2) == "22"  # still "22" after two steps

def test_iterate_term_invalid_iterations():
    import pytest
    with pytest.raises(ValueError, match="iterations must be non-negative"):
        iterate_term("1", -1)  # negative iterations

def test_iterate_term_invalid_term():
    import pytest
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate_term("", 1)  # empty term
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate_term("abc", 1)  # non-digit characters
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate_term("1a", 1)  # non-digit characters