import pytest
from solution import generate_diamond

def test_generate_diamond_A():
    # Diamond for A is a single character A
    expected = "A"
    result = generate_diamond('A')
    assert result == expected

def test_generate_diamond_B():
    # Diamond for B has three rows: 
    # 1st row:  A (1 space)
    # 2nd row: B B (0 spaces)
    # 3rd row:  A (1 space)
    expected = " A\nB B\n A"
    result = generate_diamond('B')
    assert result == expected

def test_generate_diamond_C():
    # Diamond for C has five rows:
    # 1st row:   A (2 spaces)
    # 2nd row:  B B (1 space)
    # 3rd row: C   C (0 spaces)
    # 4th row:  B B (1 space)
    # 5th row:   A (2 spaces)
    expected = "  A\n B B\nC   C\n B B\n  A"
    result = generate_diamond('C')
    assert result == expected

def test_generate_diamond_D():
    # Diamond for D has seven rows:
    # 1st row:    A (3 spaces)
    # 2nd row:   B B (2 spaces)
    # 3rd row:  C   C (1 space)
    # 4th row: D     D (0 spaces)
    # 5th row:  C   C (1 space)
    # 6th row:   B B (2 spaces)
    # 7th row:    A (3 spaces)
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    result = generate_diamond('D')
    assert result == expected

def test_generate_diamond_E():
    # Diamond for E has nine rows:
    # 1st row:     A (4 spaces)
    # 2nd row:    B B (3 spaces)
    # 3rd row:   C   C (2 spaces)
    # 4th row:  D     D (1 space)
    # 5th row: E       E (0 spaces)
    # 6th row:  D     D (1 space)
    # 7th row:   C   C (2 spaces)
    # 8th row:    B B (3 spaces)
    # 9th row:     A (4 spaces)
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    result = generate_diamond('E')
    assert result == expected

def test_generate_diamond_Z():
    # Diamond for Z has 51 rows:
    # 1st row:                                               A (25 spaces)
    # 2nd row:                                              B B (24 spaces)
    # ...
    # 49th row:                                           Y Y (24 spaces)
    # 50th row:                                              B B (24 spaces)
    # 51st row:                                               A (25 spaces)
    expected_rows = []
    for i in range(26):
        letter = chr(ord('A') + i)
        if i == 0:
            expected_rows.append(" " * (25) + letter)
        else:
            interior_spaces = " " * (2 * (i - 1) + 1)  # Adjusted for correct spacing
            expected_rows.append(" " * (25 - i) + letter + interior_spaces + letter)
    
    # Add the mirrored part
    expected_rows += expected_rows[-2::-1]
    expected = "\n".join(expected_rows)
    
    result = generate_diamond('Z')
    assert result == expected

def test_generate_diamond_lowercase_a():
    # Lowercase 'a' should return the same as uppercase 'A'
    expected = "A"
    result = generate_diamond('a')
    assert result == expected

def test_generate_diamond_lowercase_e():
    # Lowercase 'e' should return the same as uppercase 'E'
    expected = "    A\n   B B\n  C   C\n D     D\nE       E\n D     D\n  C   C\n   B B\n    A"
    result = generate_diamond('e')
    assert result == expected

def test_generate_diamond_lowercase_z():
    # Lowercase 'z' should return the same as uppercase 'Z'
    expected_rows = []
    for i in range(26):
        letter = chr(ord('A') + i)
        if i == 0:
            expected_rows.append(" " * (25) + letter)
        else:
            interior_spaces = " " * (2 * (i - 1) + 1)  # Adjusted for correct spacing
            expected_rows.append(" " * (25 - i) + letter + interior_spaces + letter)
    
    # Add the mirrored part
    expected_rows += expected_rows[-2::-1]
    expected = "\n".join(expected_rows)

    result = generate_diamond('z')
    assert result == expected

def test_generate_diamond_invalid_input_integer():
    # Invalid input: integer should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_diamond(1)
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_generate_diamond_invalid_input_empty_string():
    # Invalid input: empty string should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_diamond("")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_generate_diamond_invalid_input_multiple_characters():
    # Invalid input: multiple characters should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_diamond("AB")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_generate_diamond_invalid_input_non_letter():
    # Invalid input: non-letter should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_diamond("!")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_generate_diamond_invalid_input_whitespace():
    # Invalid input: whitespace should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_diamond(" ")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_generate_diamond_invalid_input_uppercase_invalid():
    # Invalid input: an uppercase letter that does not have a valid mapping (ß)
    with pytest.raises(Exception) as exc_info:
        generate_diamond("ß")
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_generate_diamond_invalid_input_digit_string():
    # Invalid input: digit string should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_diamond("1")
    assert str(exc_info.value) == "Input must be a single letter A-Z"