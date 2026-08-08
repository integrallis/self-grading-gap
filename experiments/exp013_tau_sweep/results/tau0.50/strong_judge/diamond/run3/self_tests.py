import pytest
from solution import generate_alphabet_diamond

def test_diamond_for_A():
    # A diamond for A is a single character A
    expected = "A"
    assert generate_alphabet_diamond('A') == expected

def test_diamond_for_B():
    # For B, the diamond is:
    #  A
    # B B
    #  A
    expected = " A\nB B\n A"
    assert generate_alphabet_diamond('B') == expected

def test_diamond_for_C():
    # For C, the diamond is:
    #   A
    #  B B
    # C   C
    #  B B
    #   A
    expected = "  A\n B B\nC   C\n B B\n  A"
    assert generate_alphabet_diamond('C') == expected

def test_diamond_for_D():
    # For D, the diamond is:
    #    A
    #   B B
    #  C   C
    # D     D
    #  C   C
    #   B B
    #    A
    expected = "   A\n  B B\n C   C\nD     D\n C   C\n  B B\n   A"
    assert generate_alphabet_diamond('D') == expected

def test_diamond_for_E():
    # For E, the diamond is:
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
    assert generate_alphabet_diamond('E') == expected

def test_diamond_for_Z():
    # For Z, the diamond has 51 rows, with the widest row being:
    # Z followed by 49 spaces and Z
    # The first and last rows are A
    # The overall shape follows the diamond pattern
    diamond = generate_alphabet_diamond('Z')
    rows = diamond.splitlines()
    assert len(rows) == 51  # 2Z - 1
    assert rows[0] == "A"  # First row
    assert rows[-1] == "A"  # Last row
    assert rows[25] == "Z" + " " * 49 + "Z"  # The middle row for Z

def test_lowercase_input():
    # Lowercase 'a' should yield the same as uppercase 'A'
    expected = "A"
    assert generate_alphabet_diamond('a') == expected

def test_invalid_input_empty_string():
    # An empty string should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_multiple_characters():
    # Multiple characters should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('AB')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_non_letter():
    # Non-letter input should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('1')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_lowercase_non_letter():
    # Lowercase non-letter input should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('@')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_special_characters():
    # Special character input should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('#')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_whitespace():
    # Whitespace input should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond(' ')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_invalid_input_ss_character():
    # Non-letter input like 'ß' should raise an error
    with pytest.raises(Exception) as exc_info:
        generate_alphabet_diamond('ß')
    assert str(exc_info.value) == "Input must be a single letter A-Z"

def test_geometry_tests():
    for target in ['A', 'B', 'C', 'D', 'E', 'F', 'M', 'Y', 'Z']:
        diamond = generate_alphabet_diamond(target)
        rows = diamond.splitlines()
        n = ord(target) - ord('A') + 1
        width = 2 * n - 1
        
        assert len(rows) == 2 * n - 1  # AC-2.1
        assert len(rows[n - 1]) == width  # AC-2.1
        assert rows[0] == "A"  # AC-2.2
        assert rows[-1] == "A"  # AC-2.2
        assert rows[0] == rows[-1]  # AC-2.4
        
        for i in range(1, n - 1):
            assert len(rows[i].replace(" ", "")) == 2  # AC-2.3
            assert rows[i] == rows[2 * n - 2 - i]  # AC-2.4
        
        assert rows == rows[::-1]  # AC-2.4
        for row in rows:
            padded = row.ljust(width)
            assert padded == padded[::-1]  # AC-2.5
        assert all(row[0] == ' ' * (n - 1 - i) + row.strip() for i, row in enumerate(rows[:n]))  # AC-2.6
        assert all(row.strip().count(' ') == (2 * i - 1) for i, row in enumerate(rows[1:n-1], start=1))  # AC-2.6
        assert all(row.rstrip() == row for row in rows)  # AC-2.8