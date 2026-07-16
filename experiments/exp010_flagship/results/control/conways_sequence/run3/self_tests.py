from solution import read_term, iterate

def test_read_term_single_digit():
    assert read_term("1") == "11"  # one 1
    assert read_term("2") == "12"  # one 2
    assert read_term("9") == "19"  # one 9

def test_read_term_repeated_digits():
    assert read_term("11") == "21"  # two 1s
    assert read_term("21") == "1211"  # one 2, one 1
    assert read_term("1211") == "111221"  # one 1, one 2, two 1s
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1
    assert read_term("3211") == "131221"  # one 3, one 2, two 1s

def test_read_term_long_runs():
    assert read_term("1111111111") == "1011"  # ten 1s
    assert read_term("00000") == "50"  # five 0s
    assert read_term("99999") == "59"  # five 9s

def test_read_term_fixed_point():
    assert read_term("22") == "22"  # fixed point

def test_iterate_zero_iterations():
    assert iterate("1", 0) == "1"  # zero iterations return the seed unchanged
    assert iterate("2", 0) == "2"  # zero iterations return the seed unchanged

def test_iterate_steps():
    assert iterate("1", 1) == "11"  # one step
    assert iterate("1", 2) == "21"  # two steps
    assert iterate("1", 5) == "312211"  # five steps
    assert iterate("2", 1) == "12"  # one step from "2"
    assert iterate("22", 3) == "22"  # fixed point after three steps

def test_iterate_fixed_point():
    assert iterate("22", 1) == "22"  # fixed point after one step
    assert iterate("22", 10) == "22"  # fixed point after ten steps

def test_invalid_negative_iterations():
    import pytest
    with pytest.raises(ValueError, match="iterations must be non-negative"):
        iterate("1", -1)

def test_invalid_empty_term():
    import pytest
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate("", 1)

def test_invalid_non_digit_term():
    import pytest
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate("12a", 1)
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate("abc", 1)
    with pytest.raises(ValueError, match="term must be a non-empty string of digits"):
        iterate("12.3", 1)