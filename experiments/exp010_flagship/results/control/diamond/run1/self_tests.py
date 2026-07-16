from solution import generate_diamond
import pytest

def test_diamond_A():
    # For letter A, the diamond is:
    expected = "A"
    assert generate_diamond('A') == expected

def test_diamond_B():
    # For letter B, the diamond is:
    expected = " A \nB B\n A "
    assert generate_diamond('B') == expected

def test_diamond_C():
    # For letter C, the diamond is:
    expected = "  A  \n B B \nC   C\n B B \n  A  "
    assert generate_diamond('C') == expected

def test_diamond_D():
    # For letter D, the diamond is:
    expected = "   A   \n  B B  \n C   C \nD     D\n C   C \n  B B  \n   A   "
    assert generate_diamond('D') == expected

def test_diamond_E():
    # For letter E, the diamond is:
    expected = "    A    \n   B B   \n  C   C  \n D     D \nE       E\n D     D \n  C   C  \n   B B   \n    A    "
    assert generate_diamond('E') == expected

def test_diamond_Z():
    # For letter Z, the diamond has 51 rows, the widest row has Z and 49 spaces
    expected = "                                                  A                                                  \n                                                 B B                                                 \n                                                C   C                                                \n                                               D     D                                               \n                                              E       E                                              \n                                             F         F                                             \n                                            G           G                                            \n                                           H             H                                           \n                                          I               I                                          \n                                         J                 J                                         \n                                        K                   K                                        \n                                       L                     L                                       \n                                      M                       M                                      \n                                     N                         N                                     \n                                    O                           O                                    \n                                   P                             P                                   \n                                  Q                               Q                                  \n                                 R                                 R                                 \n                                S                                   S                                \n                               T                                     T                               \n                              U                                       U                              \n                             V                                         V                             \n                            W                                           W                            \n                           X                                             X                           \n                          Y                                               Y                          \n                         Z                                                 Z                         \n                          Y                                               Y                          \n                           X                                             X                           \n                            W                                           W                            \n                             V                                         V                             \n                              U                                       U                              \n                               T                                     T                               \n                                S                                   S                                \n                                 R                                 R                                 \n                                  Q                               Q                                  \n                                   P                             P                                   \n                                    O                           O                                    \n                                     N                         N                                     \n                                      M                       M                                      \n                                       L                     L                                       \n                                        K                   K                                        \n                                         J                 J                                         \n                                          I               I                                          \n                                           H             H                                           \n                                            G           G                                            \n                                             F         F                                             \n                                              E       E                                              \n                                               D     D                                               \n                                                C   C                                                \n                                                 B B                                                 \n                                                  A                                                  "
    assert generate_diamond('Z') == expected

def test_diamond_lowercase_A():
    # Lowercase 'a' should produce the same diamond as 'A'
    expected = "A"
    assert generate_diamond('a') == expected

def test_diamond_invalid_input_not_single_letter():
    # Input that is not a single letter should raise an error
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_diamond('AA')

def test_diamond_invalid_input_empty_string():
    # Empty string should raise an error
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_diamond('')

def test_diamond_invalid_input_non_alpha():
    # Non-alphabetical characters should raise an error
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_diamond('1')

def test_diamond_invalid_input_unexpected_character():
    # Unexpected characters should raise an error
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_diamond('@')