from solution import render_roman_numeral

def test_render_roman_numeral_plain_values():
    assert render_roman_numeral(1) == "I"  # 1 is I
    assert render_roman_numeral(3) == "III"  # 3 is III
    assert render_roman_numeral(6) == "VI"  # 6 is VI
    assert render_roman_numeral(20) == "XX"  # 20 is XX
    assert render_roman_numeral(30) == "XXX"  # 30 is XXX
    assert render_roman_numeral(100) == "C"  # 100 is C
    assert render_roman_numeral(1000) == "M"  # 1000 is M
    assert render_roman_numeral(27) == "XXVII"  # 27 is XXVII

def test_render_roman_numeral_subtractive_notation():
    assert render_roman_numeral(4) == "IV"  # 4 is IV
    assert render_roman_numeral(9) == "IX"  # 9 is IX
    assert render_roman_numeral(40) == "XL"  # 40 is XL
    assert render_roman_numeral(90) == "XC"  # 90 is XC
    assert render_roman_numeral(400) == "CD"  # 400 is CD
    assert render_roman_numeral(900) == "CM"  # 900 is CM

def test_render_roman_numeral_composite_numbers():
    assert render_roman_numeral(49) == "XLIX"  # 49 is XLIX
    assert render_roman_numeral(87) == "LXXXVII"  # 87 is LXXXVII
    assert render_roman_numeral(239) == "CCXXXIX"  # 239 is CCXXXIX
    assert render_roman_numeral(444) == "CDXLIV"  # 444 is CDXLIV
    assert render_roman_numeral(692) == "DCXCII"  # 692 is DCXCII
    assert render_roman_numeral(999) == "CMXCIX"  # 999 is CMXCIX
    assert render_roman_numeral(2016) == "MMXVI"  # 2016 is MMXVI