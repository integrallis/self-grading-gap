from solution import read_term, iterate_from_seed
import pytest

def test_read_term_single_digit():
    assert read_term("1") == "11"  # one 1 is read as "11"
    assert read_term("2") == "12"  # one 2 is read as "12"
    assert read_term("3") == "13"  # one 3 is read as "13"
    assert read_term("0") == "10"  # one 0 is read as "10"
    assert read_term("9") == "19"  # one 9 is read as "19"

def test_read_term_multiple_identical_digits():
    assert read_term("11") == "21"  # two 1s are read as "21"
    assert read_term("22") == "22"  # two 2s read as themselves
    assert read_term("111") == "31"  # three 1s are read as "31"
    assert read_term("222") == "32"  # three 2s are read as "32"
    assert read_term("1111") == "41"  # four 1s are read as "41"
    assert read_term("000") == "30"  # three 0s are read as "30"

def test_read_term_mixed_runs():
    assert read_term("21") == "1211"  # one 2, one 1 are read as "1211"
    assert read_term("1211") == "111221"  # one 1, one 2, two 1s read as "111221"
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1 read as "312211"
    assert read_term("3211") == "131221"  # one 3, two 2s, one 1 read as "131221"

def test_read_term_large_runs():
    assert read_term("1111111111") == "101"  # ten 1s read as "101"
    assert read_term("10") == "1110"  # one 1, one 0 read as "1110"

def test_iterate_from_seed_zero_iterations():
    assert iterate_from_seed("1", 0) == "1"  # zero iterations return the seed unchanged
    assert iterate_from_seed("22", 0) == "22"  # fixed point survives zero iterations

def test_iterate_from_seed_iterations():
    assert iterate_from_seed("1", 1) == "11"  # one step from "1" gives "11"
    assert iterate_from_seed("1", 2) == "21"  # two steps give "21"
    assert iterate_from_seed("1", 5) == "312211"  # five steps give "312211"
    assert iterate_from_seed("2", 1) == "12"  # one step from "2" gives "12"
    assert iterate_from_seed("22", 3) == "22"  # fixed point after three steps remains "22"

def test_input_validation_negative_iterations():
    with pytest.raises(Exception) as excinfo:
        iterate_from_seed("1", -1)
    assert str(excinfo.value) == "iterations must be non-negative"

def test_input_validation_invalid_term():
    with pytest.raises(Exception) as excinfo:
        iterate_from_seed("", 1)  # empty string
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        iterate_from_seed("1a", 1)  # non-digit included
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        iterate_from_seed("abc", 1)  # all non-digits
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        iterate_from_seed("A1", 1)  # uppercase letter included
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        iterate_from_seed("1!", 1)  # non-digit special character included
    assert str(excinfo.value) == "term must be a non-empty string of digits"

def test_input_validation_invalid_term_single_step():
    with pytest.raises(Exception) as excinfo:
        read_term("")  # empty string
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        read_term("1a")  # non-digit included
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        read_term("abc")  # all non-digits
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        read_term("A1")  # uppercase letter included
    assert str(excinfo.value) == "term must be a non-empty string of digits"

    with pytest.raises(Exception) as excinfo:
        read_term("1!")  # non-digit special character included
    assert str(excinfo.value) == "term must be a non-empty string of digits"