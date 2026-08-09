from solution import convert_to_roman

def test_convert_to_roman_for_1():
    assert convert_to_roman(1) == 'I'  # 1 is I

def test_convert_to_roman_for_3():
    assert convert_to_roman(3) == 'III'  # 3 is III

def test_convert_to_roman_for_4():
    assert convert_to_roman(4) == 'IV'  # 4 is IV

def test_convert_to_roman_for_6():
    assert convert_to_roman(6) == 'VI'  # 6 is VI

def test_convert_to_roman_for_9():
    assert convert_to_roman(9) == 'IX'  # 9 is IX

def test_convert_to_roman_for_20():
    assert convert_to_roman(20) == 'XX'  # 20 is XX

def test_convert_to_roman_for_30():
    assert convert_to_roman(30) == 'XXX'  # 30 is XXX

def test_convert_to_roman_for_40():
    assert convert_to_roman(40) == 'XL'  # 40 is XL

def test_convert_to_roman_for_50():
    assert convert_to_roman(50) == 'L'  # 50 is L

def test_convert_to_roman_for_87():
    assert convert_to_roman(87) == 'LXXXVII'  # 87 is LXXXVII

def test_convert_to_roman_for_100():
    assert convert_to_roman(100) == 'C'  # 100 is C

def test_convert_to_roman_for_239():
    assert convert_to_roman(239) == 'CCXXXIX'  # 239 is CCXXXIX

def test_convert_to_roman_for_400():
    assert convert_to_roman(400) == 'CD'  # 400 is CD

def test_convert_to_roman_for_444():
    assert convert_to_roman(444) == 'CDXLIV'  # 444 is CDXLIV

def test_convert_to_roman_for_500():
    assert convert_to_roman(500) == 'D'  # 500 is D

def test_convert_to_roman_for_692():
    assert convert_to_roman(692) == 'DCXCII'  # 692 is DCXCII

def test_convert_to_roman_for_900():
    assert convert_to_roman(900) == 'CM'  # 900 is CM

def test_convert_to_roman_for_999():
    assert convert_to_roman(999) == 'CMXCIX'  # 999 is CMXCIX

def test_convert_to_roman_for_1000():
    assert convert_to_roman(1000) == 'M'  # 1000 is M

def test_convert_to_roman_for_2016():
    assert convert_to_roman(2016) == 'MMXVI'  # 2016 is MMXVI

def test_convert_to_roman_for_27():
    assert convert_to_roman(27) == 'XXVII'  # 27 is XXVII

def test_convert_to_roman_for_90():
    assert convert_to_roman(90) == 'XC'  # 90 is XC

def test_convert_to_roman_for_49():
    assert convert_to_roman(49) == 'XLIX'  # 49 is XLIX