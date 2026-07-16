import pytest
from solution import last_sundays_of_year, last_sunday_of_month

def test_last_sundays_of_year():
    # Test for the year 2013
    # Expected: 2013-01-27, 2013-02-24, 2013-03-31, 2013-04-28, 
    # 2013-05-26, 2013-06-30, 2013-07-28, 2013-08-25, 
    # 2013-09-29, 2013-10-27, 2013-11-24, 2013-12-29
    assert list(last_sundays_of_year(2013)) == [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28", 
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25", 
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]

    # Test for the leap year 2032
    # Expected: 2032-01-25, 2032-02-29, 2032-03-28, 2032-04-25, 
    # 2032-05-30, 2032-06-27, 2032-07-25, 2032-08-29, 
    # 2032-09-26, 2032-10-31, 2032-11-28, 2032-12-26
    assert list(last_sundays_of_year(2032)) == [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25", 
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29", 
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]

    # Test for the year 2100 (not a leap year)
    # Expected: 2100-01-31, 2100-02-28, 2100-03-28, 2100-04-25, 
    # 2100-05-30, 2100-06-27, 2100-07-25, 2100-08-29, 
    # 2100-09-26, 2100-10-31, 2100-11-28, 2100-12-26
    assert list(last_sundays_of_year(2100)) == [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25", 
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29", 
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]

    # Test December 2000, which has December 31 as a Sunday
    # Expected: 2000-12-31
    assert list(last_sundays_of_year(2000))[-1] == "2000-12-31"

def test_last_sunday_of_month():
    # Test last Sunday for January 2013
    # Expected: 2013-01-27
    assert last_sunday_of_month(2013, 1) == "2013-01-27"
    
    # Test last Sunday for March 2013
    # Expected: 2013-03-31
    assert last_sunday_of_month(2013, 3) == "2013-03-31"
    
    # Test last Sunday for February 2024 (leap year)
    # Expected: 2024-02-25 (February 29 is on a weekday)
    assert last_sunday_of_month(2024, 2) == "2024-02-25"
    
    # Test last Sunday for February 2032 (leap year)
    # Expected: 2032-02-29 (February 29 is a Sunday)
    assert last_sunday_of_month(2032, 2) == "2032-02-29"

    # Test last Sunday for February 2100 (not a leap year)
    # Expected: 2100-02-28
    assert last_sunday_of_month(2100, 2) == "2100-02-28"

    # Test for an out-of-range month (13)
    # Expected: error with message "month must be in 1..12"
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        last_sunday_of_month(2013, 13)

    # Test for an out-of-range month (0)
    # Expected: error with message "month must be in 1..12"
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        last_sunday_of_month(2013, 0)