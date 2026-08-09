from solution import read_term, iterate_from_seed

def test_read_term_single_digit():
    assert read_term("1") == "11"  # one 1 becomes "11"
    assert read_term("2") == "12"  # one 2 becomes "12"
    assert read_term("3") == "13"  # one 3 becomes "13"
    assert read_term("4") == "14"  # one 4 becomes "14"
    assert read_term("5") == "15"  # one 5 becomes "15"
    assert read_term("6") == "16"  # one 6 becomes "16"
    assert read_term("7") == "17"  # one 7 becomes "17"
    assert read_term("8") == "18"  # one 8 becomes "18"
    assert read_term("9") == "19"  # one 9 becomes "19"

def test_read_term_multiple_identical_digits():
    assert read_term("11") == "21"  # two 1s become "21"
    assert read_term("111") == "31"  # three 1s become "31"
    assert read_term("1111") == "41"  # four 1s become "41"
    assert read_term("222") == "32"  # three 2s become "32"
    assert read_term("2222") == "42"  # four 2s become "42"

def test_read_term_mixed_digits():
    assert read_term("21") == "1211"  # one 2, one 1 becomes "1211"
    assert read_term("1211") == "111221"  # one 1, one 2, two 1s becomes "111221"
    assert read_term("111221") == "312211"  # three 1s, two 2s, one 1 becomes "312211"
    assert read_term("3211") == "131221"  # one 3, one 2, two 1s becomes "131221"

def test_read_term_fixed_point():
    assert read_term("22") == "22"  # remains "22"

def test_read_term_runs_with_ten_or_more():
    assert read_term("0000000000") == "100"  # ten 0s become "100"
    assert read_term("1111111111") == "101"  # ten 1s become "101"
    assert read_term("11111111111") == "111"  # eleven 1s become "111"

def test_read_term_zero_and_nine():
    assert read_term("10") == "1110"  # one 1, one 0 becomes "1110"
    assert read_term("9") == "19"  # one 9 becomes "19"

def test_iterate_from_seed_zero_iterations():
    assert iterate_from_seed("1", 0) == "1"  # seed unchanged
    assert iterate_from_seed("2", 0) == "2"  # seed unchanged
    assert iterate_from_seed("22", 0) == "22"  # seed unchanged

def test_iterate_from_seed_multiple_iterations():
    assert iterate_from_seed("1", 1) == "11"  # one iteration gives "11"
    assert iterate_from_seed("1", 2) == "21"  # two iterations give "21"
    assert iterate_from_seed("1", 5) == "312211"  # five iterations give "312211"
    assert iterate_from_seed("2", 1) == "12"  # one iteration gives "12"
    assert iterate_from_seed("22", 1) == "22"  # remains "22"

def test_iterate_from_seed_fixed_point():
    assert iterate_from_seed("22", 3) == "22"  # remains "22" after three steps

def test_input_validation_negative_iterations():
    import pytest
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1", -1)
    assert str(exc.value) == "iterations must be non-negative"

def test_input_validation_invalid_term_empty():
    import pytest
    with pytest.raises(Exception) as exc:
        iterate_from_seed("", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"

def test_input_validation_invalid_term_non_digit():
    import pytest
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1a", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    with pytest.raises(Exception) as exc:
        iterate_from_seed("1.5", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    with pytest.raises(Exception) as exc:
        iterate_from_seed("2#", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"
    with pytest.raises(Exception) as exc:
        iterate_from_seed("A", 1)
    assert str(exc.value) == "term must be a non-empty string of digits"

def test_read_term_invalid_term_empty():
    import pytest
    with pytest.raises(Exception) as exc:
        read_term("")
    assert str(exc.value) == "term must be a non-empty string of digits"

def test_read_term_invalid_term_non_digit():
    import pytest
    with pytest.raises(Exception) as exc:
        read_term("1a")
    assert str(exc.value) == "term must be a non-empty string of digits"
    with pytest.raises(Exception) as exc:
        read_term("1.5")
    assert str(exc.value) == "term must be a non-empty string of digits"
    with pytest.raises(Exception) as exc:
        read_term("2#")
    assert str(exc.value) == "term must be a non-empty string of digits"
    with pytest.raises(Exception) as exc:
        read_term("A")
    assert str(exc.value) == "term must be a non-empty string of digits"