from solution import read_term, iterate_from_seed

def test_read_term():
    # AC-1.1
    assert read_term("1") == "11"         # "1" -> "11"
    assert read_term("11") == "21"        # "11" -> "21"
    assert read_term("21") == "1211"      # "21" -> "1211"
    assert read_term("1211") == "111221"  # "1211" -> "111221"
    assert read_term("111221") == "312211" # "111221" -> "312211"
    assert read_term("2") == "12"         # "2" -> "12"
    assert read_term("3211") == "131221"  # "3211" -> "131221"
    
    # AC-1.2
    assert read_term("1111111111") == "101"  # ten 1s -> "101"
    
    # AC-1.3
    assert read_term("22") == "22"        # "22" -> "22" (fixed point)
    
    # AC-1.4
    assert read_term("10") == "1110"      # "10" -> "1110"
    assert read_term("9") == "19"         # "9" -> "19"

def test_iterate_from_seed():
    # AC-2.1
    assert iterate_from_seed("1", 0) == "1"  # Zero iterations return the seed unchanged
    
    # AC-2.2
    assert iterate_from_seed("1", 1) == "11"  # one step: "1" -> "11"
    assert iterate_from_seed("1", 2) == "21"  # two steps: "1" -> "11" -> "21"
    assert iterate_from_seed("1", 5) == "312211"  # five steps: "1" -> "11" -> "21" -> "1211" -> "111221" -> "312211"
    
    assert iterate_from_seed("2", 1) == "12"  # one step: "2" -> "12"
    
    # AC-2.3
    assert iterate_from_seed("22", 3) == "22"  # three steps: "22" -> "22" (fixed point)

def test_invalid_inputs():
    # AC-3.1
    try:
        iterate_from_seed("1", -1)
    except ValueError as e:
        assert str(e) == "iterations must be non-negative"  # Negative iteration count
    
    # AC-3.2
    try:
        iterate_from_seed("", 1)
    except ValueError as e:
        assert str(e) == "term must be a non-empty string of digits"  # Empty term
    
    try:
        iterate_from_seed("1a", 1)
    except ValueError as e:
        assert str(e) == "term must be a non-empty string of digits"  # Non-digit character
    
    try:
        iterate_from_seed(" ", 1)
    except ValueError as e:
        assert str(e) == "term must be a non-empty string of digits"  # Non-digit character