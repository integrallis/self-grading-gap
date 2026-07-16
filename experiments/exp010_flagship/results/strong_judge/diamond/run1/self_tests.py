import pytest
from solution import generate_alphabet_diamond

def test_diamond_for_A():
    # For letter A, the diamond is a single character A.
    expected = "A"
    assert generate_alphabet_diamond("A") == expected

def test_diamond_for_B():
    # For letter B, the diamond is:
    #  A
    # B B
    #  A
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond("B") == expected

def test_diamond_for_C():
    # For letter C, the diamond is:
    #   A
    #  B B
    # C   C
    #  B B
    #   A
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_alphabet_diamond("C") == expected

def test_diamond_for_D():
    # For letter D, the diamond is:
    #    A
    #   B B
    #  C   C
    # D     D
    #  C   C
    #   B B
    #    A
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    assert generate_alphabet_diamond("D") == expected

def test_diamond_for_E():
    # For letter E, the diamond is:
    #    A
    #   B B
    #  C   C
    # D     D
    # E       E
    # D     D
    #  C   C
    #   B B
    #    A
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    assert generate_alphabet_diamond("E") == expected

def test_diamond_for_Z():
    # For letter Z, the diamond has 51 rows, and the widest row is a Z, 49 spaces, and a Z.
    result = generate_alphabet_diamond("Z")
    rows = result.splitlines()
    assert len(rows) == 51  # 2Z-1 rows
    assert len(rows[25]) == 51  # Middle row (Z) should be 51 characters wide
    assert rows[25] == "Z" + " " * 49 + "Z"  # Check the content of the middle row

def test_lowercase_input():
    # Lowercase 'a' should produce the same diamond as uppercase 'A'.
    expected = "A"
    assert generate_alphabet_diamond("a") == expected
    
    # Lowercase 'b' should produce the same diamond as uppercase 'B'.
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond("b") == expected

    # Lowercase 'm' should produce the same diamond as uppercase 'M'.
    expected = "     A\n    B B\n   C   C\n  D     D\n E       E\nD     D\n C   C\n  B B\n   A"
    assert generate_alphabet_diamond("m") == expected

    # Lowercase 'y' should produce the same diamond as uppercase 'Y'.
    expected = "                    A\n                   B B\n                  C   C\n                 D     D\n                E       E\n               F         F\n              G           G\n             H             H\n            I               I\n           J                 J\n          K                   K\n         L                     L\n        M                       M\n       N                         N\n      O                           O\n     P                             P\n    Q                               Q\n   R                                 R\n  S                                   S\n T                                     T\nU                                       U\n T                                     T\n  S                                   S\n   R                                 R\n    Q                               Q\n     P                             P\n      O                           O\n       N                         N\n        M                       M\n         L                     L\n          K                   K\n           J                 J\n            I               I\n             H             H\n              G           G\n               F         F\n                E       E\n                 D     D\n                  C   C\n                   B B\n                    A"
    assert generate_alphabet_diamond("y") == expected

def test_invalid_input_not_a_single_letter():
    # Input '1' is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("1")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input 'ab' is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("ab")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input '' (empty string) is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input ' ' (whitespace) is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond(" ")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_non_letter():
    # Input '%' is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("%")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input 'ß' is invalid as it uppercases to 'SS'
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("ß")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input 'é' is invalid as it uppercases to 'E'
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("é")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input tab character is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("\t")
    assert str(exc.value) == "Input must be a single letter A-Z"

    # Input newline character is invalid
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("\n")
    assert str(exc.value) == "Input must be a single letter A-Z"