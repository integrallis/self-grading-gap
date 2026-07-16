from solution import generate_alphabet_diamond

def test_generate_diamond_A():
    # Diamond for A
    expected = "A\n"
    assert generate_alphabet_diamond('A') == expected

def test_generate_diamond_B():
    # Diamond for B
    expected = " A \nB B\n A \n"
    assert generate_alphabet_diamond('B') == expected

def test_generate_diamond_C():
    # Diamond for C
    expected = "  A  \n B B \nC   C\n B B \n  A  \n"
    assert generate_alphabet_diamond('C') == expected

def test_generate_diamond_D():
    # Diamond for D
    expected = "   A   \n  B B  \n C   C \nD     D\n C   C \n  B B  \n   A   \n"
    assert generate_alphabet_diamond('D') == expected

def test_generate_diamond_E():
    # Diamond for E
    expected = "    A    \n   B B   \n  C   C  \n D     D \nE       E\n D     D \n  C   C  \n   B B   \n    A    \n"
    assert generate_alphabet_diamond('E') == expected

def test_generate_diamond_Z():
    # Diamond for Z (51 rows total, widest row is Z followed by 49 spaces and another Z)
    expected = "                                                  A                                                  \n" + \
               "                                                 B B                                                 \n" + \
               "                                                C   C                                                \n" + \
               "                                               D     D                                               \n" + \
               "                                              E       E                                              \n" + \
               "                                             F         F                                             \n" + \
               "                                            G           G                                            \n" + \
               "                                           H             H                                           \n" + \
               "                                          I               I                                          \n" + \
               "                                         J                 J                                         \n" + \
               "                                        K                   K                                        \n" + \
               "                                       L                     L                                       \n" + \
               "                                      M                       M                                      \n" + \
               "                                     N                         N                                     \n" + \
               "                                    O                           O                                    \n" + \
               "                                   P                             P                                   \n" + \
               "                                  Q                               Q                                  \n" + \
               "                                 R                                 R                                 \n" + \
               "                                S                                   S                                \n" + \
               "                               T                                     T                               \n" + \
               "                              U                                       U                              \n" + \
               "                             V                                         V                             \n" + \
               "                            W                                           W                            \n" + \
               "                           X                                             X                           \n" + \
               "                          Y                                               Y                          \n" + \
               "                         Z                                                 Z                         \n" + \
               "                          Y                                               Y                          \n" + \
               "                           X                                             X                           \n" + \
               "                            W                                           W                            \n" + \
               "                             V                                         V                             \n" + \
               "                              U                                       U                              \n" + \
               "                               T                                     T                               \n" + \
               "                                S                                   S                                \n" + \
               "                                 R                                 R                                 \n" + \
               "                                  Q                               Q                                  \n" + \
               "                                   P                             P                                   \n" + \
               "                                    O                           O                                    \n" + \
               "                                     N                         N                                     \n" + \
               "                                      M                       M                                      \n" + \
               "                                       L                     L                                       \n" + \
               "                                        K                   K                                        \n" + \
               "                                         J                 J                                         \n" + \
               "                                          I               I                                          \n" + \
               "                                           H             H                                           \n" + \
               "                                            G           G                                            \n" + \
               "                                             F         F                                             \n" + \
               "                                              E       E                                              \n" + \
               "                                               D     D                                               \n" + \
               "                                                C   C                                                \n" + \
               "                                                 B B                                                 \n" + \
               "                                                  A                                                  \n"
    assert generate_alphabet_diamond('Z') == expected

def test_generate_diamond_lowercase_a():
    # Lowercase a should produce the same diamond as uppercase A
    expected = "A\n"
    assert generate_alphabet_diamond('a') == expected

def test_generate_diamond_lowercase_b():
    # Lowercase b should produce the same diamond as uppercase B
    expected = " A \nB B\n A \n"
    assert generate_alphabet_diamond('b') == expected

def test_invalid_input_empty():
    # Invalid input: empty string
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_alphabet_diamond('')

def test_invalid_input_multiple_characters():
    # Invalid input: multiple characters
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_alphabet_diamond('AB')

def test_invalid_input_digit():
    # Invalid input: digit
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_alphabet_diamond('1')

def test_invalid_input_special_character():
    # Invalid input: special character
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_alphabet_diamond('@')

def test_invalid_input_uppercase_with_multiple_uppercase():
    # Invalid input: character that uppercases to multiple letters
    with pytest.raises(ValueError, match="Input must be a single letter A-Z"):
        generate_alphabet_diamond('ß')