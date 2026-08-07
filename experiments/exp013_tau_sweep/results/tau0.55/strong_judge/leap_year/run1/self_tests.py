import pytest
from solution import leap_year  # Assuming the function name is `leap_year`

def test_non_century_leap_year_divisible_by_four():
    # 1992 is divisible by 4, so it is a leap year
    assert leap_year(1992) == True

def test_non_century_leap_year_divisible_by_four_2():
    # 1996 is divisible by 4, so it is a leap year
    assert leap_year(1996) == True

def test_non_leap_year_not_divisible_by_four():
    # 2001 is not divisible by 4, so it is not a leap year
    assert leap_year(2001) == False

def test_non_leap_year_not_divisible_by_four_2():
    # 2005 is not divisible by 4, so it is not a leap year
    assert leap_year(2005) == False

def test_non_leap_year_not_divisible_by_four_3():
    # 2013 is not divisible by 4, so it is not a leap year
    assert leap_year(2013) == False

def test_century_year_not_divisible_by_400():
    # 1900 is a century year and not divisible by 400, so it is not a leap year
    assert leap_year(1900) == False

def test_century_year_divisible_by_400():
    # 1600 is a century year and divisible by 400, so it is a leap year
    assert leap_year(1600) == True

def test_century_year_divisible_by_400_2():
    # 2000 is a century year and divisible by 400, so it is a leap year
    assert leap_year(2000) == True

def test_century_year_not_divisible_by_400_2():
    # 2100 is a century year and not divisible by 400, so it is not a leap year
    assert leap_year(2100) == False

@pytest.mark.parametrize("year, expected", [
    (2004, True),   # 2004 is divisible by 4, so it is a leap year
    (2014, False),  # 2014 is not divisible by 4, so it is not a leap year
    (2200, False),  # 2200 is a century year not divisible by 400, so it is not a leap year
    (2400, True)    # 2400 is a century year divisible by 400, so it is a leap year
])
def test_parameterized_years(year, expected):
    assert leap_year(year) == expected