# test_solution.py

from solution import to_roman

def test_to_roman_1():
    assert to_roman(1) == "I"  # 1 is I

def test_to_roman_3():
    assert to_roman(3) == "III"  # 3 is III

def test_to_roman_4():
    assert to_roman(4) == "IV"  # 4 is IV

def test_to_roman_6():
    assert to_roman(6) == "VI"  # 6 is VI

def test_to_roman_9():
    assert to_roman(9) == "IX"  # 9 is IX

def test_to_roman_20():
    assert to_roman(20) == "XX"  # 20 is XX

def test_to_roman_30():
    assert to_roman(30) == "XXX"  # 30 is XXX

def test_to_roman_40():
    assert to_roman(40) == "XL"  # 40 is XL

def test_to_roman_87():
    assert to_roman(87) == "LXXXVII"  # 87 is LXXXVII

def test_to_roman_100():
    assert to_roman(100) == "C"  # 100 is C

def test_to_roman_239():
    assert to_roman(239) == "CCXXXIX"  # 239 is CCXXXIX

def test_to_roman_400():
    assert to_roman(400) == "CD"  # 400 is CD

def test_to_roman_444():
    assert to_roman(444) == "CDXLIV"  # 444 is CDXLIV

def test_to_roman_500():
    assert to_roman(500) == "D"  # 500 is D

def test_to_roman_692():
    assert to_roman(692) == "DCXCII"  # 692 is DCXCII

def test_to_roman_900():
    assert to_roman(900) == "CM"  # 900 is CM

def test_to_roman_999():
    assert to_roman(999) == "CMXCIX"  # 999 is CMXCIX

def test_to_roman_1000():
    assert to_roman(1000) == "M"  # 1000 is M

def test_to_roman_2016():
    assert to_roman(2016) == "MMXVI"  # 2016 is MMXVI