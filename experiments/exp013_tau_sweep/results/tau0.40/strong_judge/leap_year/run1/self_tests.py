# test_leap_year.py

from solution import is_leap_year

def test_leap_year_divisible_by_four():
    # 1992 is divisible by 4, so it is a leap year
    assert is_leap_year(1992) == True
    # 1996 is divisible by 4, so it is a leap year
    assert is_leap_year(1996) == True

def test_non_leap_year_not_divisible_by_four():
    # 2001 is not divisible by 4, so it is not a leap year
    assert is_leap_year(2001) == False
    # 2005 is not divisible by 4, so it is not a leap year
    assert is_leap_year(2005) == False
    # 2013 is not divisible by 4, so it is not a leap year
    assert is_leap_year(2013) == False

def test_century_year_not_divisible_by_400():
    # 1900 is a century year and not divisible by 400, so it is not a leap year
    assert is_leap_year(1900) == False
    # 2100 is a century year and not divisible by 400, so it is not a leap year
    assert is_leap_year(2100) == False

def test_century_year_divisible_by_400():
    # 1600 is a century year and divisible by 400, so it is a leap year
    assert is_leap_year(1600) == True
    # 2000 is a century year and divisible by 400, so it is a leap year
    assert is_leap_year(2000) == True