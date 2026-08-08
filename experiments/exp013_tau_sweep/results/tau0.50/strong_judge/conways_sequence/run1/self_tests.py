from solution import read_term_aloud, iterate_from_seed

def test_read_term_aloud():
    # AC-1.1
    assert read_term_aloud("1") == "11"          # one 1
    assert read_term_aloud("11") == "21"         # two 1s
    assert read_term_aloud("21") == "1211"       # one 2, then one 1
    assert read_term_aloud("1211") == "111221"   # one 1, one 2, two 1s
    assert read_term_aloud("111221") == "312211"  # three 1s, two 2s, one 1
    assert read_term_aloud("2") == "12"          # one 2
    assert read_term_aloud("3211") == "131221"   # one 3, one 2, two 1s
    
    # AC-1.2
    assert read_term_aloud("1111111111") == "101"  # ten 1s
    assert read_term_aloud("2222222222") == "102"  # ten 2s

    # AC-1.3
    assert read_term_aloud("22") == "22"          # fixed point

    # AC-1.4
    assert read_term_aloud("10") == "1110"        # one 1, one 0
    assert read_term_aloud("9") == "19"           # one 9

def test_iterate_from_seed():
    # AC-2.1
    assert iterate_from_seed("1", 0) == "1"       # zero iterations
    
    # AC-2.2
    assert iterate_from_seed("1", 1) == "11"      # one step from "1"
    assert iterate_from_seed("1", 2) == "21"      # two steps from "1"
    assert iterate_from_seed("1", 5) == "312211"   # five steps from "1"
    assert iterate_from_seed("2", 1) == "12"      # one step from "2"

    # AC-2.3
    assert iterate_from_seed("22", 3) == "22"     # three steps from fixed point "22"

def test_input_validation():
    # AC-3.1
    try:
        iterate_from_seed("1", -1)
    except Exception as e:
        assert str(e) == "iterations must be non-negative"  # Check message if an exception is raised
    else:
        assert False, "Expected an exception for negative iterations"

    # AC-3.2
    try:
        iterate_from_seed("", 1)
    except Exception as e:
        assert str(e) == "term must be a non-empty string of digits"  # Check message if an exception is raised
    else:
        assert False, "Expected an exception for empty term"
    
    try:
        iterate_from_seed("1a", 1)
    except Exception as e:
        assert str(e) == "term must be a non-empty string of digits"  # Check message if an exception is raised
    else:
        assert False, "Expected an exception for non-digit character in term"

    try:
        iterate_from_seed("12.3", 1)
    except Exception as e:
        assert str(e) == "term must be a non-empty string of digits"  # Check message if an exception is raised
    else:
        assert False, "Expected an exception for non-digit character in term"

    try:
        read_term_aloud("")
    except Exception as e:
        assert str(e) == "term must be a non-empty string of digits"  # Check message if an exception is raised
    else:
        assert False, "Expected an exception for empty term"

    try:
        read_term_aloud("1A")
    except Exception as e:
        assert str(e) == "term must be a non-empty string of digits"  # Check message if an exception is raised
    else:
        assert False, "Expected an exception for non-digit character in term"