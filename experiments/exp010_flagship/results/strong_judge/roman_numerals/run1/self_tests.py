from solution import convert_to_roman

def test_convert_to_roman_1():
    # 1 is I
    assert convert_to_roman(1) == "I"

def test_convert_to_roman_3():
    # 3 is III
    assert convert_to_roman(3) == "III"

def test_convert_to_roman_4():
    # 4 is IV
    assert convert_to_roman(4) == "IV"

def test_convert_to_roman_6():
    # 6 is VI
    assert convert_to_roman(6) == "VI"

def test_convert_to_roman_9():
    # 9 is IX
    assert convert_to_roman(9) == "IX"

def test_convert_to_roman_20():
    # 20 is XX
    assert convert_to_roman(20) == "XX"

def test_convert_to_roman_30():
    # 30 is XXX
    assert convert_to_roman(30) == "XXX"

def test_convert_to_roman_40():
    # 40 is XL
    assert convert_to_roman(40) == "XL"

def test_convert_to_roman_50():
    # 50 is L
    assert convert_to_roman(50) == "L"

def test_convert_to_roman_90():
    # 90 is XC
    assert convert_to_roman(90) == "XC"

def test_convert_to_roman_100():
    # 100 is C
    assert convert_to_roman(100) == "C"

def test_convert_to_roman_400():
    # 400 is CD
    assert convert_to_roman(400) == "CD"

def test_convert_to_roman_500():
    # 500 is D
    assert convert_to_roman(500) == "D"

def test_convert_to_roman_900():
    # 900 is CM
    assert convert_to_roman(900) == "CM"

def test_convert_to_roman_1000():
    # 1000 is M
    assert convert_to_roman(1000) == "M"

def test_convert_to_roman_27():
    # 27 is XXVII
    assert convert_to_roman(27) == "XXVII"

def test_convert_to_roman_49():
    # 49 is XLIX
    assert convert_to_roman(49) == "XLIX"

def test_convert_to_roman_58():
    # 58 is LVIII
    assert convert_to_roman(58) == "LVIII"

def test_convert_to_roman_87():
    # 87 is LXXXVII
    assert convert_to_roman(87) == "LXXXVII"

def test_convert_to_roman_239():
    # 239 is CCXXXIX
    assert convert_to_roman(239) == "CCXXXIX"

def test_convert_to_roman_444():
    # 444 is CDXLIV
    assert convert_to_roman(444) == "CDXLIV"

def test_convert_to_roman_692():
    # 692 is DCXCII
    assert convert_to_roman(692) == "DCXCII"

def test_convert_to_roman_999():
    # 999 is CMXCIX
    assert convert_to_roman(999) == "CMXCIX"

def test_convert_to_roman_2016():
    # 2016 is MMXVI
    assert convert_to_roman(2016) == "MMXVI"

def test_convert_to_roman_1994():
    # 1994 is MCMXCIV
    assert convert_to_roman(1994) == "MCMXCIV"