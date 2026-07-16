import pytest
from solution import generate_alphabet_diamond

def test_diamond_for_A():
    # A diamond for A is a single character A
    expected = "A"
    actual = generate_alphabet_diamond("A")
    assert actual == expected

def test_diamond_for_B():
    # A diamond for B has 3 rows: A, B B, A
    expected = " A\nB B\n A"
    actual = generate_alphabet_diamond("B")
    assert actual == expected

def test_diamond_for_C():
    # A diamond for C has 5 rows: A, B B, C   C, B B, A
    expected = "  A\n B B\nC   C\n B B\n  A"
    actual = generate_alphabet_diamond("C")
    assert actual == expected

def test_diamond_for_D():
    # A diamond for D has 7 rows: A, B B, C   C, D     D, C   C, B B, A
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    actual = generate_alphabet_diamond("D")
    assert actual == expected

def test_diamond_for_E():
    # A diamond for E has 9 rows: A, B B, C   C, D     D, E       E, D     D, C   C, B B, A
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    actual = generate_alphabet_diamond("E")
    assert actual == expected

def test_diamond_for_F():
    # A diamond for F has 11 rows: A, B B, C   C, D     D, E       E, F         F, E       E, D     D, C   C, B B, A
    expected = "     A\n    B B\n   C   C\n  D     D\n E       E\nF         F\n E       E\n  D     D\n   C   C\n    B B\n     A"
    actual = generate_alphabet_diamond("F")
    assert actual == expected

def test_diamond_for_Z():
    # A diamond for Z has 51 rows, with the widest row being Z and 49 spaces
    expected = "                                                  A\n" + \
               "                                                 B B\n" + \
               "                                                C   C\n" + \
               "                                               D     D\n" + \
               "                                              E       E\n" + \
               "                                             F         F\n" + \
               "                                            G           G\n" + \
               "                                           H             H\n" + \
               "                                          I               I\n" + \
               "                                         J                 J\n" + \
               "                                        K                   K\n" + \
               "                                       L                     L\n" + \
               "                                      M                       M\n" + \
               "                                     N                         N\n" + \
               "                                    O                           O\n" + \
               "                                   P                             P\n" + \
               "                                  Q                               Q\n" + \
               "                                 R                                 R\n" + \
               "                                S                                   S\n" + \
               "                               T                                     T\n" + \
               "                              U                                       U\n" + \
               "                             V                                         V\n" + \
               "                            W                                           W\n" + \
               "                           X                                             X\n" + \
               "                          Y                                               Y\n" + \
               "                         Z                                                 Z\n" + \
               "                          Y                                               Y\n" + \
               "                           X                                             X\n" + \
               "                            W                                           W\n" + \
               "                             V                                         V\n" + \
               "                              U                                       U\n" + \
               "                               T                                     T\n" + \
               "                                S                                   S\n" + \
               "                                 R                                 R\n" + \
               "                                  Q                               Q\n" + \
               "                                   P                             P\n" + \
               "                                    O                           O\n" + \
               "                                     N                         N\n" + \
               "                                      M                       M\n" + \
               "                                       L                     L\n" + \
               "                                        K                   K\n" + \
               "                                         J                 J\n" + \
               "                                          I               I\n" + \
               "                                           H             H\n" + \
               "                                            G           G\n" + \
               "                                             F         F\n" + \
               "                                              E       E\n" + \
               "                                               D     D\n" + \
               "                                                C   C\n" + \
               "                                                 B B\n" + \
               "                                                  A"
    actual = generate_alphabet_diamond("Z")
    assert actual == expected

def test_lowercase_input():
    # A lowercase letter produces the same diamond as its uppercase form
    expected = " A\nB B\n A"
    actual = generate_alphabet_diamond("b")
    assert actual == expected

def test_invalid_input_empty():
    # Input that is not a single letter (empty string) should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_multiple_characters():
    # Input that is not a single letter (multiple characters) should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("AB")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_non_letter():
    # Input that is not a single letter (non-letter character) should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("1")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_special_character():
    # Input that is not a single letter (special character) should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("@")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_uppercase_conversion():
    # A single character that uppercases to more than one letter should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("ß")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_whitespace():
    # Input that is not a single letter (whitespace) should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond(" ")
    assert str(exc.value) == "Input must be a single letter A-Z"

def test_invalid_input_unicode():
    # Input that is a single non-A–Z Unicode letter should be rejected
    with pytest.raises(Exception) as exc:
        generate_alphabet_diamond("é")
    assert str(exc.value) == "Input must be a single letter A-Z"