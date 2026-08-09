import pytest
from solution import generate_alphabet_diamond

def test_diamond_for_A():
    # A diamond for A has 1 row: "A"
    expected = "A"
    assert generate_alphabet_diamond('A') == expected

def test_diamond_for_B():
    # A diamond for B has 3 rows: 
    # " A"
    # "B B"
    # " A"
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond('B') == expected

def test_diamond_for_C():
    # A diamond for C has 5 rows:
    # "  A"
    # " B B"
    # "C   C"
    # " B B"
    # "  A"
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_alphabet_diamond('C') == expected

def test_diamond_for_D():
    # A diamond for D has 7 rows:
    # "   A"
    # "  B B"
    # " C   C"
    # "D     D"
    # " C   C"
    # "  B B"
    # "   A"
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    assert generate_alphabet_diamond('D') == expected

def test_diamond_for_E():
    # A diamond for E has 9 rows:
    # "    A"
    # "   B B"
    # "  C   C"
    # " D     D"
    # "E       E"
    # " D     D"
    # "  C   C"
    # "   B B"
    # "    A"
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    assert generate_alphabet_diamond('E') == expected

def test_diamond_for_Z():
    # A diamond for Z has 51 rows, with the widest row being "Z" and 49 spaces
    # The first and last rows will be: "                         A"
    # The middle row will be: "Z                                               Z"
    expected_first_last = " " * 25 + "A"
    expected_middle = "Z" + " " * 49 + "Z"
    
    diamond = generate_alphabet_diamond('Z')
    rows = diamond.splitlines()
    
    assert len(rows) == 51
    assert rows[0] == expected_first_last
    assert rows[-1] == expected_first_last
    assert rows[25] == expected_middle

def test_lowercase_input():
    # Lowercase 'e' should produce the same diamond as uppercase 'E'
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    assert generate_alphabet_diamond('e') == expected

def test_invalid_input_not_single_letter():
    # Input of length not equal to 1 should raise an error.
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('AB')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('1')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('!')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond(' ')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_uppercase_multiple_letters():
    # Character that uppercases to more than one letter should raise an error.
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('ß')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_non_ascii_input():
    # One-character non-ASCII input that uppercases to one character should raise an error.
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('é')
    assert str(exc_info.value) == "Input must be a single letter A-Z"