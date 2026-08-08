import pytest
from solution import generate_alphabet_diamond

def test_diamond_for_A():
    # Expected diamond for A:
    # A
    expected = "A"
    assert generate_alphabet_diamond("A") == expected

def test_diamond_for_B():
    # Expected diamond for B:
    #  A
    # B B
    #  A
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond("B") == expected

def test_diamond_for_C():
    # Expected diamond for C:
    #   A
    #  B B
    # C   C
    #  B B
    #   A
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_alphabet_diamond("C") == expected

def test_diamond_for_D():
    # Expected diamond for D:
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
    # Expected diamond for E:
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

def test_diamond_for_Z():
    # Expected diamond for Z:
    #                                                  A
    #                                                 B B
    #                                                C   C
    #                                               D     D
    #                                              E       E
    #                                             F         F
    #                                            G           G
    #                                           H             H
    #                                          I               I
    #                                         J                 J
    #                                        K                   K
    #                                       L                     L
    #                                      M                       M
    #                                     N                         N
    #                                    O                           O
    #                                   P                             P
    #                                  Q                               Q
    #                                 R                                 R
    #                                S                                   S
    #                               T                                     T
    #                              U                                       U
    #                             V                                         V
    #                            W                                           W
    #                           X                                             X
    #                          Y                                               Y
    #                         Z                                                 Z
    #                          Y                                               Y
    #                           X                                             X
    #                            W                                           W
    #                             V                                         V
    #                              U                                       U
    #                               T                                     T
    #                                S                                   S
    #                                 R                                 R
    #                                  Q                               Q
    #                                   P                             P
    #                                    O                           O
    #                                     N                         N
    #                                      M                       M
    #                                       L                     L
    #                                        K                   K
    #                                         J                 J
    #                                          I               I
    #                                           H             H
    #                                            G           G
    #                                             F         F
    #                                              E       E
    #                                               D     D
    #                                                C   C
    #                                                 B B
    #                                                  A
    expected = (
        "                                                  A\n"
        "                                                 B B\n"
        "                                                C   C\n"
        "                                               D     D\n"
        "                                              E       E\n"
        "                                             F         F\n"
        "                                            G           G\n"
        "                                           H             H\n"
        "                                          I               I\n"
        "                                         J                 J\n"
        "                                        K                   K\n"
        "                                       L                     L\n"
        "                                      M                       M\n"
        "                                     N                         N\n"
        "                                    O                           O\n"
        "                                   P                             P\n"
        "                                  Q                               Q\n"
        "                                 R                                 R\n"
        "                                S                                   S\n"
        "                               T                                     T\n"
        "                              U                                       U\n"
        "                             V                                         V\n"
        "                            W                                           W\n"
        "                           X                                             X\n"
        "                          Y                                               Y\n"
        "                         Z                                                 Z\n"
        "                          Y                                               Y\n"
        "                           X                                             X\n"
        "                            W                                           W\n"
        "                             V                                         V\n"
        "                              U                                       U\n"
        "                               T                                     T\n"
        "                                S                                   S\n"
        "                                 R                                 R\n"
        "                                  Q                               Q\n"
        "                                   P                             P\n"
        "                                    O                           O\n"
        "                                     N                         N\n"
        "                                      M                       M\n"
        "                                       L                     L\n"
        "                                        K                   K\n"
        "                                         J                 J\n"
        "                                          I               I\n"
        "                                           H             H\n"
        "                                            G           G\n"
        "                                             F         F\n"
        "                                              E       E\n"
        "                                               D     D\n"
        "                                                C   C\n"
        "                                                 B B\n"
        "                                                  A"
    )
    assert generate_alphabet_diamond("Z") == expected

def test_lowercase_A():
    # Lowercase 'a' should produce the same as uppercase 'A'
    expected = "A"
    assert generate_alphabet_diamond("a") == expected

def test_lowercase_B():
    # Lowercase 'b' should produce the same as uppercase 'B'
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond("b") == expected

def test_lowercase_M():
    # Lowercase 'm' should produce the same as uppercase 'M'
    expected = (
        "           A\n"
        "          B B\n"
        "         C   C\n"
        "        D     D\n"
        "       E       E\n"
        "      F         F\n"
        "     G           G\n"
        "    H             H\n"
        "   I               I\n"
        "  J                 J\n"
        " K                   K\n"
        "L                     L\n"
        "M                       M\n"
        " L                     L\n"
        "  K                   K\n"
        "   J                 J\n"
        "    I               I\n"
        "     H             H\n"
        "      G           G\n"
        "       F         F\n"
        "        E       E\n"
        "         D     D\n"
        "          C   C\n"
        "           B B\n"
        "            A"
    )
    assert generate_alphabet_diamond("m") == expected

def test_invalid_input_not_a_single_letter():
    # Should raise an unspecified exception for input that is not a single letter
    invalid_inputs = ["", "1", "AB", " ", "@", "ß", "\t", "\n"]
    for input in invalid_inputs:
        with pytest.raises(Exception) as excinfo:
            generate_alphabet_diamond(input)
        assert str(excinfo.value) == "Input must be a single letter A-Z"

def test_invalid_input_non_uppercase_letter():
    # Should raise an unspecified exception for a character that uppercases to more than one letter
    with pytest.raises(Exception) as excinfo:
        generate_alphabet_diamond("ß")
    assert str(excinfo.value) == "Input must be a single letter A-Z"