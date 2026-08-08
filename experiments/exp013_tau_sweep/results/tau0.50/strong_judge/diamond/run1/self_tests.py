from solution import generate_alphabet_diamond
import pytest

def test_diamond_A():
    # For the letter A, the diamond is a single character A
    expected = "A"
    assert generate_alphabet_diamond("A") == expected

def test_diamond_B():
    # For the letter B, the diamond is:
    #  A
    # B B
    #  A
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond("B") == expected

def test_diamond_C():
    # For the letter C, the diamond is:
    #   A
    #  B B
    # C   C
    #  B B
    #   A
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_alphabet_diamond("C") == expected

def test_diamond_D():
    # For the letter D, the diamond is:
    #    A
    #   B B
    #  C   C
    # D     D
    #  C   C
    #   B B
    #    A
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    assert generate_alphabet_diamond("D") == expected

def test_diamond_E():
    # For the letter E, the diamond is:
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
    assert generate_alphabet_diamond("E") == expected

def test_diamond_Z():
    # For the letter Z, the diamond has 51 rows, with the widest row being Z, 49 spaces, and a Z
    expected = "                         A\n" + \
               "                        B B\n" + \
               "                       C   C\n" + \
               "                      D     D\n" + \
               "                     E       E\n" + \
               "                    F         F\n" + \
               "                   G           G\n" + \
               "                  H             H\n" + \
               "                 I               I\n" + \
               "                J                 J\n" + \
               "               K                   K\n" + \
               "              L                     L\n" + \
               "             M                       M\n" + \
               "            N                         N\n" + \
               "           O                           O\n" + \
               "          P                             P\n" + \
               "         Q                               Q\n" + \
               "        R                                 R\n" + \
               "       S                                   S\n" + \
               "      T                                     T\n" + \
               "     U                                       U\n" + \
               "    V                                         V\n" + \
               "   W                                           W\n" + \
               "  X                                             X\n" + \
               " Y                                               Y\n" + \
               "Z                                                 Z\n" + \
               " Y                                               Y\n" + \
               "  X                                             X\n" + \
               "   W                                           W\n" + \
               "    V                                         V\n" + \
               "     U                                       U\n" + \
               "      T                                     T\n" + \
               "       S                                   S\n" + \
               "        R                                 R\n" + \
               "         Q                               Q\n" + \
               "          P                             P\n" + \
               "           O                           O\n" + \
               "            N                         N\n" + \
               "             M                       M\n" + \
               "              L                     L\n" + \
               "               K                   K\n" + \
               "                J                 J\n" + \
               "                 I               I\n" + \
               "                  H             H\n" + \
               "                   G           G\n" + \
               "                    F         F\n" + \
               "                     E       E\n" + \
               "                      D     D\n" + \
               "                       C   C\n" + \
               "                        B B\n" + \
               "                         A"
    assert generate_alphabet_diamond("Z") == expected

def test_lowercase_input():
    # Lowercase input 'a' should produce the same diamond as 'A'
    expected = "A"
    assert generate_alphabet_diamond("a") == expected

@pytest.mark.parametrize("input_letter", [chr(letter) for letter in range(ord('F'), ord('Y') + 1)])
def test_valid_uppercase_targets(input_letter):
    # Check properties for valid uppercase letters F through Y
    diamond = generate_alphabet_diamond(input_letter)
    N = ord(input_letter) - ord('A') + 1
    expected_row_count = 2 * N - 1
    expected_widest_row = input_letter + " " * (2 * N - 3) + input_letter if N > 1 else input_letter

    # Check row count
    assert diamond.count('\n') + 1 == expected_row_count

    # Check widest row
    assert len(max(diamond.splitlines(), key=len)) == len(expected_widest_row)

    # Check alphabetical row sequence and symmetry
    rows = diamond.splitlines()
    assert rows == rows[::-1]  # Check vertical symmetry

    # Check absence of trailing spaces
    for row in rows:
        assert row == row.rstrip()

def test_invalid_input_too_many_characters():
    # Input that is not a single letter should raise an exception with the specified message
    import pytest
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond("")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_non_letter():
    # Input that is not a single letter should raise an exception with the specified message
    import pytest
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond("1")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_multiple_characters():
    # Input that is not a single letter should raise an exception with the specified message
    import pytest
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond("AB")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_special_character():
    # Input that is not a single letter should raise an exception with the specified message
    import pytest
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond("@")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_uppercase_non_single():
    # Input that is a single character that uppercases to more than one letter should raise an exception with the specified message
    import pytest
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond("ß")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_whitespace():
    # Input that is a whitespace should raise an exception with the specified message
    import pytest
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond(" ")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_lowercase_non_A_input():
    # Lowercase input 'b' should produce the same diamond as 'B'
    assert generate_alphabet_diamond("b") == generate_alphabet_diamond("B")