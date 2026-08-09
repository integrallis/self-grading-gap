import pytest
from solution import read_term, iterate

def test_read_term_single_digit():
    assert read_term("1") == "11"  # one 1 becomes "11"
    assert read_term("2") == "12"  # one 2 becomes "12"
    assert read_term("9") == "19"  # one 9 becomes "19"
    assert read_term("0") == "10"  # one 0 becomes "10"

def test_read_term_multiple_identical_digits():
    assert read_term("11") == "21"  # two 1s become "21"
    assert read_term("222") == "32"  # three 2s become "32"
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1 becomes "312211"
    assert read_term("3211") == "131221"  # one 3, two 1s becomes "131221"

def test_read_term_runs_of_ten_or_more():
    assert read_term("1111111111") == "101"  # ten 1s become "101"
    assert read_term("0000000000") == "100"  # ten 0s become "100"
    assert read_term("11111111111") == "111"  # eleven 1s become "111"

def test_read_term_fixed_points():
    assert read_term("22") == "22"  # "22" is unchanged

def test_read_term_other_cases():
    assert read_term("10") == "1110"  # one 1, one 0 becomes "1110"
    assert read_term("21") == "1211"  # one 2, one 1 becomes "1211"
    assert read_term("1211") == "111221"  # one 1, one 2, two 1s becomes "111221"

def test_iterate_zero_iterations():
    assert iterate("1", 0) == "1"  # zero iterations return the seed unchanged
    assert iterate("22", 0) == "22"  # fixed point survives zero iterations

def test_iterate_multiple_iterations():
    assert iterate("1", 1) == "11"  # one step from "1" gives "11"
    assert iterate("1", 2) == "21"  # two steps from "1" gives "21"
    assert iterate("1", 5) == "312211"  # five steps from "1" gives "312211"
    assert iterate("2", 1) == "12"  # one step from "2" gives "12"
    assert iterate("22", 3) == "22"  # three steps from fixed point "22" still gives "22"

def test_invalid_inputs():
    # Negative iterations
    with pytest.raises(ValueError, match=r"^iterations must be non-negative$"):
        iterate("1", -1)
    
    # Invalid term inputs
    with pytest.raises(ValueError, match=r"^term must be a non-empty string of digits$"):
        iterate("", 1)  # empty string
    with pytest.raises(ValueError, match=r"^term must be a non-empty string of digits$"):
        iterate("1A", 1)  # contains an uppercase letter
    with pytest.raises(ValueError, match=r"^term must be a non-empty string of digits$"):
        iterate("1a", 1)  # contains a lowercase letter
    with pytest.raises(ValueError, match=r"^term must be a non-empty string of digits$"):
        iterate("1.5", 1)  # contains a decimal
    with pytest.raises(ValueError, match=r"^term must be a non-empty string of digits$"):
        iterate(" ", 1)  # contains a space
    with pytest.raises(ValueError, match=r"^term must be a non-empty string of digits$"):
        iterate("1", 0)  # invalid term with zero iterations