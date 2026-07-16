from solution import leap_year

def test_non_century_year_divisible_by_four_is_leap_year():
    # 1992 is divisible by 4, so it is a leap year
    assert leap_year(1992) == True

def test_another_non_century_year_divisible_by_four_is_leap_year():
    # 1996 is divisible by 4, so it is a leap year
    assert leap_year(1996) == True

def test_year_not_divisible_by_four_is_not_leap_year():
    # 2001 is not divisible by 4, so it is not a leap year
    assert leap_year(2001) == False

def test_another_year_not_divisible_by_four_is_not_leap_year():
    # 2005 is not divisible by 4, so it is not a leap year
    assert leap_year(2005) == False

def test_yet_another_year_not_divisible_by_four_is_not_leap_year():
    # 2013 is not divisible by 4, so it is not a leap year
    assert leap_year(2013) == False

def test_century_year_not_divisible_by_400_is_not_leap_year():
    # 1900 is a century year and not divisible by 400, so it is not a leap year
    assert leap_year(1900) == False

def test_another_century_year_not_divisible_by_400_is_not_leap_year():
    # 2100 is a century year and not divisible by 400, so it is not a leap year
    assert leap_year(2100) == False

def test_century_year_divisible_by_400_is_leap_year():
    # 1600 is a century year and divisible by 400, so it is a leap year
    assert leap_year(1600) == True

def test_another_century_year_divisible_by_400_is_leap_year():
    # 2000 is a century year and divisible by 400, so it is a leap year
    assert leap_year(2000) == True

def test_non_century_year_divisible_by_four_is_leap_year_2024():
    # 2024 is divisible by 4, so it is a leap year
    assert leap_year(2024) == True

def test_year_not_divisible_by_four_is_not_leap_year_2023():
    # 2023 is not divisible by 4, so it is not a leap year
    assert leap_year(2023) == False

def test_century_year_not_divisible_by_400_is_not_leap_year_2200():
    # 2200 is a century year and not divisible by 400, so it is not a leap year
    assert leap_year(2200) == False

def test_century_year_divisible_by_400_is_leap_year_2400():
    # 2400 is a century year and divisible by 400, so it is a leap year
    assert leap_year(2400) == True