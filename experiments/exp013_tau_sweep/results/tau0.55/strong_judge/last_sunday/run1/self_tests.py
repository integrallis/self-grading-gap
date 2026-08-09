import pytest
from solution import last_sundays_of_year, last_sunday_of_month

# US-1: List a year's last Sundays
def test_last_sundays_of_year_2013():
    # Expected: 2013-01-27, 2013-02-24, 2013-03-31, 2013-04-28, 
    # 2013-05-26, 2013-06-30, 2013-07-28, 2013-08-25, 
    # 2013-09-29, 2013-10-27, 2013-11-24, 2013-12-29
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28", 
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25", 
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert last_sundays_of_year(2013) == expected

def test_last_sundays_of_year_2032():
    # Expected: 2032-01-25, 2032-02-29, 2032-03-28, 2032-04-25, 
    # 2032-05-30, 2032-06-27, 2032-07-25, 2032-08-29, 
    # 2032-09-26, 2032-10-31, 2032-11-28, 2032-12-26
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25", 
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29", 
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert last_sundays_of_year(2032) == expected

def test_last_sundays_of_year_2100():
    # Expected: 2100-01-31, 2100-02-28, 2100-03-28, 2100-04-25, 
    # 2100-05-30, 2100-06-27, 2100-07-25, 2100-08-29, 
    # 2100-09-26, 2100-10-31, 2100-11-28, 2100-12-26
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25", 
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29", 
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert last_sundays_of_year(2100) == expected

def test_last_sundays_of_year_2000():
    # Expected: 2000-01-30, 2000-02-27, 2000-03-26, 2000-04-30, 
    # 2000-05-28, 2000-06-25, 2000-07-30, 2000-08-27, 
    # 2000-09-24, 2000-10-29, 2000-11-26, 2000-12-31
    expected = [
        "2000-01-30", "2000-02-27", "2000-03-26", "2000-04-30", 
        "2000-05-28", "2000-06-25", "2000-07-30", "2000-08-27", 
        "2000-09-24", "2000-10-29", "2000-11-26", "2000-12-31"
    ]
    assert last_sundays_of_year(2000) == expected

# US-3: Look up a single month
def test_last_sunday_of_month_2013_january():
    # Expected: 2013-01-27
    assert last_sunday_of_month(2013, 1) == "2013-01-27"

def test_last_sunday_of_month_2013_march():
    # Expected: 2013-03-31
    assert last_sunday_of_month(2013, 3) == "2013-03-31"

def test_last_sunday_of_month_2024_february_leap():
    # Expected: 2024-02-25 (Feb 29 is a Thursday)
    assert last_sunday_of_month(2024, 2) == "2024-02-25"

def test_last_sunday_of_month_2032_february_leap():
    # Expected: 2032-02-29 (Feb 29 is a Sunday)
    assert last_sunday_of_month(2032, 2) == "2032-02-29"

def test_last_sunday_of_month_out_of_range():
    # Expected: error message "month must be in 1..12"
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        last_sunday_of_month(2022, 13)

def test_last_sunday_of_month_zero():
    # Expected: error message "month must be in 1..12"
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        last_sunday_of_month(2022, 0)