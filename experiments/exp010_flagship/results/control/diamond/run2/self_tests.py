from solution import generate_alphabet_diamond

def test_diamond_for_A():
    expected = "A"
    # The diamond for A is simply "A"
    assert generate_alphabet_diamond('A') == expected

def test_diamond_for_B():
    expected = " A\nB B\n A"
    # The diamond for B:
    # Row 1: " A" (1 space + A)
    # Row 2: "B B" (B + space + B)
    # Row 3: " A" (1 space + A)
    assert generate_alphabet_diamond('B') == expected

def test_diamond_for_C():
    expected = "  A\n B B\nC   C\n B B\n  A"
    # The diamond for C:
    # Row 1: "  A" (2 spaces + A)
    # Row 2: " B B" (1 space + B + space + B)
    # Row 3: "C   C" (C + 3 spaces + C)
    # Row 4: " B B" (1 space + B + space + B)
    # Row 5: "  A" (2 spaces + A)
    assert generate_alphabet_diamond('C') == expected

def test_diamond_for_D():
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    # The diamond for D:
    # Row 1: "   A" (3 spaces + A)
    # Row 2: "  B B" (2 spaces + B + space + B)
    # Row 3: " C   C" (C + 3 spaces + C)
    # Row 4: "D     D" (D + 5 spaces + D)
    # Row 5: " C   C" (C + 3 spaces + C)
    # Row 6: "  B B" (2 spaces + B + space + B)
    # Row 7: "   A" (3 spaces + A)
    assert generate_alphabet_diamond('D') == expected

def test_diamond_for_E():
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    # The diamond for E:
    # Row 1: "    A" (4 spaces + A)
    # Row 2: "   B B" (3 spaces + B + space + B)
    # Row 3: "  C   C" (C + 3 spaces + C)
    # Row 4: " D     D" (D + 5 spaces + D)
    # Row 5: "E       E" (E + 7 spaces + E)
    # Row 6: " D     D" (D + 5 spaces + D)
    # Row 7: "  C   C" (C + 3 spaces + C)
    # Row 8: "   B B" (3 spaces + B + space + B)
    # Row 9: "    A" (4 spaces + A)
    assert generate_alphabet_diamond('E') == expected

def test_diamond_for_Z():
    expected = "                                                  A\n                                                 B B\n                                                C   C\n                                               D     D\n                                              E       E\n                                             F         F\n                                            G           G\n                                           H             H\n                                          I               I\n                                         J                 J\n                                        K                   K\n                                       L                     L\n                                      M                       M\n                                     N                         N\n                                    O                           O\n                                   P                             P\n                                  Q                               Q\n                                 R                                 R\n                                S                                   S\n                               T                                     T\n                              U                                       U\n                             V                                         V\n                            W                                           W\n                           X                                             X\n                          Y                                               Y\n                         Z                                                 Z\n                          Y                                               Y\n                           X                                             X\n                            W                                           W\n                             V                                         V\n                              U                                       U\n                               T                                     T\n                                S                                   S\n                                 R                                 R\n                                  Q                               Q\n                                   P                             P\n                                    O                           O\n                                     N                         N\n                                      M                       M\n                                       L                     L\n                                        K                   K\n                                         J                 J\n                                          I               I\n                                           H             H\n                                            G           G\n                                             F         F\n                                              E       E\n                                               D     D\n                                                C   C\n                                                 B B\n                                                  A"
    # The diamond for Z has 51 rows:
    # Row 1: "                                                  A" (49 spaces + A)
    # ...
    # Row 51: "                                                  A" (49 spaces + A)
    assert generate_alphabet_diamond('Z') == expected

def test_lowercase_input():
    expected = " A\nB B\n A"
    # The diamond for lowercase 'b' should be the same as for uppercase 'B'
    assert generate_alphabet_diamond('b') == expected

def test_invalid_input_not_single_letter():
    with pytest.raises(ValueError) as excinfo:
        generate_alphabet_diamond('AB')
    assert str(excinfo.value) == "Input must be a single letter A-Z"

def test_invalid_input_empty_string():
    with pytest.raises(ValueError) as excinfo:
        generate_alphabet_diamond('')
    assert str(excinfo.value) == "Input must be a single letter A-Z"

def test_invalid_input_not_letter():
    with pytest.raises(ValueError) as excinfo:
        generate_alphabet_diamond('1')
    assert str(excinfo.value) == "Input must be a single letter A-Z"

def test_invalid_input_non_alpha_character():
    with pytest.raises(ValueError) as excinfo:
        generate_alphabet_diamond('@')
    assert str(excinfo.value) == "Input must be a single letter A-Z"

def test_invalid_input_uppercase_form_more_than_one_letter():
    with pytest.raises(ValueError) as excinfo:
        generate_alphabet_diamond('ß')
    assert str(excinfo.value) == "Input must be a single letter A-Z"