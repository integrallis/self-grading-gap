# test_leap_year.py

from solution import is_leap_year

def test_non_century_year_divisible_by_four_is_leap_year():
    # 1992 is divisible by 4 (1992 % 4 == 0)
    assert is_leap_year(1992) == True

def test_another_non_century_year_divisible_by_four_is_leap_year():
    # 1996 is divisible by 4 (1996 % 4 == 0)
    assert is_leap_year(1996) == True

def test_year_not_divisible_by_four_is_not_leap_year():
    # 2001 is not divisible by 4 (2001 % 4 != 0)
    assert is_leap_year(2001) == False

def test_another_year_not_divisible_by_four_is_not_leap_year():
    # 2005 is not divisible by 4 (2005 % 4 != 0)
    assert is_leap_year(2005) == False

def test_year_not_divisible_by_four_is_not_leap_year_again():
    # 2013 is not divisible by 4 (2013 % 4 != 0)
    assert is_leap_year(2013) == False

def test_century_year_not_divisible_by_400_is_not_leap_year():
    # 1900 is not divisible by 400 (1900 % 400 != 0)
    assert is_leap_year(1900) == False

def test_another_century_year_not_divisible_by_400_is_not_leap_year():
    # 2100 is not divisible by 400 (2100 % 400 != 0)
    assert is_leap_year(2100) == False

def test_century_year_divisible_by_400_is_leap_year():
    # 1600 is divisible by 400 (1600 % 400 == 0)
    assert is_leap_year(1600) == True

def test_another_century_year_divisible_by_400_is_leap_year():
    # 2000 is divisible by 400 (2000 % 400 == 0)
    assert is_leap_year(2000) == True