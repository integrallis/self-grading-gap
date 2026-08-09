from solution import is_leap_year

def test_leap_year_divisible_by_four():
    # AC-1.1: 1992 is divisible by 4, so it is a leap year
    assert is_leap_year(1992) == True
    # AC-1.1: 1996 is divisible by 4, so it is a leap year
    assert is_leap_year(1996) == True

def test_non_leap_year_not_divisible_by_four():
    # AC-1.2: 2001 is not divisible by 4, so it is not a leap year
    assert is_leap_year(2001) == False
    # AC-1.2: 2005 is not divisible by 4, so it is not a leap year
    assert is_leap_year(2005) == False
    # AC-1.2: 2013 is not divisible by 4, so it is not a leap year
    assert is_leap_year(2013) == False

def test_century_year_not_divisible_by_400():
    # AC-2.1: 1900 is a century year not divisible by 400, so it is not a leap year
    assert is_leap_year(1900) == False
    # AC-2.1: 2100 is a century year not divisible by 400, so it is not a leap year
    assert is_leap_year(2100) == False

def test_century_year_divisible_by_400():
    # AC-2.2: 1600 is a century year divisible by 400, so it is a leap year
    assert is_leap_year(1600) == True
    # AC-2.2: 2000 is a century year divisible by 400, so it is a leap year
    assert is_leap_year(2000) == True