# test_alphabet_diamond.py

import pytest
from solution import generate_diamond

def test_diamond_for_A():
    # Diamond for A is a single character A
    expected = "A"
    assert generate_diamond("A") == expected

def test_diamond_for_B():
    # Diamond for B is:
    #  A
    # B B
    #  A
    expected = " A\nB B\n A"
    assert generate_diamond("B") == expected

def test_diamond_for_C():
    # Diamond for C is:
    #   A
    #  B B
    # C   C
    #  B B
    #   A
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_diamond("C") == expected

def test_diamond_for_D():
    # Diamond for D is:
    #    A
    #   B B
    #  C   C
    # D     D
    #  C   C
    #   B B
    #    A
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    assert generate_diamond("D") == expected

def test_diamond_for_E():
    # Diamond for E is:
    #     A
    #    B B
    #   C   C
    #  D     D
    # E       E
    #  D     D
    #   C   C
    #    B B
    #     A
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    assert generate_diamond("E") == expected

def test_diamond_for_Z():
    # Diamond for Z has 51 rows, and the widest row has a Z, with 49 spaces in between.
    diamond = generate_diamond("Z")
    rows = diamond.splitlines()
    assert len(rows) == 51  # Total number of rows for Z
    assert len(rows[25]) == 51  # Middle row should have 51 characters (Z + 49 spaces + Z)
    assert rows[0] == " " * 25 + "A"  # First row structure
    assert rows[-1] == " " * 25 + "A"  # Last row structure
    assert rows[25] == "Z" + " " * 49 + "Z"  # Middle row structure

@pytest.mark.parametrize("input_char", ["a", "b", "c", "d", "e", "z"])
def test_lowercase_input(input_char):
    # Lowercase input should produce the same diamond as uppercase
    expected = generate_diamond(input_char.upper())
    assert generate_diamond(input_char) == expected

def test_invalid_inputs():
    # Input that is not a single letter A-Z should be rejected
    invalid_inputs = ["", "ab", "1", "@", " ", "ß"]
    for inp in invalid_inputs:
        with pytest.raises(Exception, match=r"^Input must be a single letter A-Z$"):
            generate_diamond(inp)

def test_invalid_uppercase_multiple_letters():
    # Input that is a single character whose uppercase form is more than one letter (like ß)
    invalid_inputs = ["ß"]
    for inp in invalid_inputs:
        with pytest.raises(Exception, match=r"^Input must be a single letter A-Z$"):
            generate_diamond(inp)

@pytest.mark.parametrize("letter", "FGHIJKLMNOPQRSTUVWXY")
def test_geometry_properties(letter):
    # General tests for geometry properties for letters F-Y
    diamond = generate_diamond(letter)
    rows = diamond.splitlines()
    
    N = ord(letter) - ord('A') + 1
    assert len(rows) == 2 * N - 1  # Total number of rows
    assert len(rows[N - 1]) == 2 * N - 1  # Middle row width
    assert rows[0] == " " * (N - 1) + "A"  # First row structure
    assert rows[-1] == " " * (N - 1) + "A"  # Last row structure
    for i in range(1, N):
        assert rows[i] == " " * (N - i - 1) + chr(ord('A') + i) + " " * (2 * i - 1) + chr(ord('A') + i)  # Upper half
        assert rows[-(i + 1)] == rows[i]  # Lower half symmetry

    # Check for trailing spaces
    for row in rows:
        assert not row.endswith(" ")  # No trailing spaces