import pytest
from solution import generate_diamond

def test_diamond_for_letter_A():
    # A diamond for the letter A is a single character A
    expected = "A"
    assert generate_diamond("A") == expected

def test_diamond_for_letter_B():
    # A diamond for the letter B is:
    expected = " A\nB B\n A"
    assert generate_diamond("B") == expected

def test_diamond_for_letter_C():
    # A diamond for the letter C is:
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_diamond("C") == expected

def test_diamond_for_letter_D():
    # A diamond for the letter D is:
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    assert generate_diamond("D") == expected

def test_diamond_for_letter_E():
    # A diamond for the letter E is:
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    assert generate_diamond("E") == expected

def test_diamond_for_letter_Z():
    # A diamond for the letter Z has 51 rows and its widest row has Z and 49 spaces.
    expected = (
        "                                                  A                                                  \n"
        "                                                 B B                                                 \n"
        "                                                C   C                                                \n"
        "                                               D     D                                               \n"
        "                                              E       E                                              \n"
        "                                             F         F                                             \n"
        "                                            G           G                                            \n"
        "                                           H             H                                           \n"
        "                                          I               I                                          \n"
        "                                         J                 J                                         \n"
        "                                        K                   K                                        \n"
        "                                       L                     L                                       \n"
        "                                      M                       M                                      \n"
        "                                     N                         N                                     \n"
        "                                    O                           O                                    \n"
        "                                   P                             P                                   \n"
        "                                  Q                               Q                                  \n"
        "                                 R                                 R                                 \n"
        "                                S                                   S                                \n"
        "                               T                                     T                               \n"
        "                              U                                       U                              \n"
        "                             V                                         V                             \n"
        "                            W                                           W                            \n"
        "                           X                                             X                           \n"
        "                          Y                                               Y                          \n"
        "                         Z                                                 Z                         \n"
        "                          Y                                               Y                          \n"
        "                           X                                             X                           \n"
        "                            W                                           W                            \n"
        "                             V                                         V                             \n"
        "                              U                                       U                              \n"
        "                               T                                     T                               \n"
        "                                S                                   S                                \n"
        "                                 R                                 R                                 \n"
        "                                  Q                               Q                                  \n"
        "                                   P                             P                                   \n"
        "                                    O                           O                                    \n"
        "                                     N                         N                                     \n"
        "                                      M                       M                                      \n"
        "                                       L                     L                                       \n"
        "                                        K                   K                                        \n"
        "                                         J                 J                                         \n"
        "                                          I               I                                          \n"
        "                                           H             H                                           \n"
        "                                            G           G                                            \n"
        "                                             F         F                                             \n"
        "                                              E       E                                              \n"
        "                                               D     D                                               \n"
        "                                                C   C                                                \n"
        "                                                 B B                                                 \n"
        "                                                  A                                                  "
    )
    assert generate_diamond("Z") == expected

def test_lowercase_input():
    # A lowercase letter produces the same diamond as its uppercase form
    expected = " A\nB B\n A"
    assert generate_diamond("b") == expected

def test_invalid_input_not_a_letter():
    # Input that is not a single letter A through Z is rejected
    error = None
    try:
        generate_diamond("1")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"

def test_invalid_input_multiple_characters():
    # Input that is more than one character is rejected
    error = None
    try:
        generate_diamond("AB")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"

def test_invalid_input_empty_string():
    # An empty string is rejected as invalid
    error = None
    try:
        generate_diamond("")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"

def test_invalid_input_uppercase_more_than_one_letter():
    # A single character whose uppercase form is more than one letter is rejected
    error = None
    try:
        generate_diamond("ß")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"

def test_invalid_input_punctuation():
    # Input that is punctuation is rejected
    error = None
    try:
        generate_diamond("!")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"

def test_invalid_input_whitespace():
    # Input that is whitespace is rejected
    error = None
    try:
        generate_diamond(" ")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"

def test_diamond_for_letter_M():
    # A diamond for the letter M is:
    expected = "       A\n      B B\n     C   C\n    D     D\n   E       E\n  F         F\n G           G\nH             H\n G           G\n  F         F\n   E       E\n    D     D\n     C   C\n      B B\n       A"
    assert generate_diamond("M") == expected

def test_invalid_input_non_ascii():
    # A non-ASCII character that is a single letter is rejected
    error = None
    try:
        generate_diamond("é")
    except Exception as e:
        error = e
    assert str(error) == "Input must be a single letter A-Z"