# test_leap_year.py

from solution import is_leap_year

def test_non_century_year_divisible_by_four_is_leap_year():
    # 1992 is divisible by 4 and not a century year, so it is a leap year.
    assert is_leap_year(1992) is True
    # 1996 is divisible by 4 and not a century year, so it is a leap year.
    assert is_leap_year(1996) is True

def test_year_not_divisible_by_four_is_not_leap_year():
    # 2001 is not divisible by 4, so it is not a leap year.
    assert is_leap_year(2001) is False
    # 2005 is not divisible by 4, so it is not a leap year.
    assert is_leap_year(2005) is False
    # 2013 is not divisible by 4, so it is not a leap year.
    assert is_leap_year(2013) is False

def test_century_year_not_divisible_by_400_is_not_leap_year():
    # 1900 is a century year but not divisible by 400, so it is not a leap year.
    assert is_leap_year(1900) is False
    # 2100 is a century year but not divisible by 400, so it is not a leap year.
    assert is_leap_year(2100) is False

def test_century_year_divisible_by_400_is_leap_year():
    # 1600 is a century year and divisible by 400, so it is a leap year.
    assert is_leap_year(1600) is True
    # 2000 is a century year and divisible by 400, so it is a leap year.
    assert is_leap_year(2000) is True