from solution import is_leap_year

def test_non_century_year_divisible_by_four_is_leap_year():
    # 1992 is divisible by 4 => leap year
    assert is_leap_year(1992) == True

def test_non_century_year_divisible_by_four_is_leap_year_2():
    # 1996 is divisible by 4 => leap year
    assert is_leap_year(1996) == True

def test_non_century_year_not_divisible_by_four_is_not_leap_year():
    # 2001 is not divisible by 4 => not a leap year
    assert is_leap_year(2001) == False

def test_non_century_year_not_divisible_by_four_is_not_leap_year_2():
    # 2005 is not divisible by 4 => not a leap year
    assert is_leap_year(2005) == False

def test_non_century_year_not_divisible_by_four_is_not_leap_year_3():
    # 2013 is not divisible by 4 => not a leap year
    assert is_leap_year(2013) == False

def test_century_year_not_divisible_by_400_is_not_leap_year():
    # 1900 is divisible by 100 but not by 400 => not a leap year
    assert is_leap_year(1900) == False

def test_century_year_not_divisible_by_400_is_not_leap_year_2():
    # 2100 is divisible by 100 but not by 400 => not a leap year
    assert is_leap_year(2100) == False

def test_century_year_divisible_by_400_is_leap_year():
    # 1600 is divisible by 400 => leap year
    assert is_leap_year(1600) == True

def test_century_year_divisible_by_400_is_leap_year_2():
    # 2000 is divisible by 400 => leap year
    assert is_leap_year(2000) == True