import pytest
from datetime import datetime
from solution import calculate_age_and_birthday_week

def test_age_in_whole_years():
    # AC-1.1
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2022, 11, 5)) == (6, "October 23, 2016")
    
    # AC-1.2: Before first anniversary
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2017, 10, 27)) == (0, "October 30, 2016")
    
    # AC-1.2: Cross-calendar-year
    assert calculate_age_and_birthday_week(datetime(2016, 12, 31), datetime(2017, 1, 1)) == (0, "December 25, 2016")
    
    # AC-1.3: Day after anniversary
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2022, 10, 28)) == (6, "October 30, 2022")
    
    # AC-1.4
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2016, 10, 28)) == (0, "October 30, 2016")

def test_leap_day_birthdays():
    # AC-2.1
    assert calculate_age_and_birthday_week(datetime(2000, 2, 29), datetime(2023, 2, 28)) == (22, "February 23, 2000")
    
    # AC-2.2
    assert calculate_age_and_birthday_week(datetime(2000, 2, 29), datetime(2024, 2, 29)) == (24, "February 23, 2000")

def test_future_birth_dates_rejected():
    # AC-3.1: Birth date after reference date
    with pytest.raises(Exception) as excinfo:
        calculate_age_and_birthday_week(datetime(2023, 10, 2), datetime(2023, 10, 1))
    assert str(excinfo.value) == "birthdate is after today"
    
    # AC-3.2: Birth date exactly one day after reference date
    with pytest.raises(Exception) as excinfo:
        calculate_age_and_birthday_week(datetime(2023, 10, 2), datetime(2023, 10, 1))
    assert str(excinfo.value) == "birthdate is after today"

def test_birthday_week_start_date():
    # AC-4.1
    assert calculate_age_and_birthday_week(datetime(2017, 9, 3), datetime(2022, 11, 5)) == (5, "August 28, 2017")
    
    # AC-4.2
    assert calculate_age_and_birthday_week(datetime(2017, 9, 7), datetime(2022, 11, 5)) == (5, "September 3, 2017")
    assert calculate_age_and_birthday_week(datetime(2017, 9, 8), datetime(2022, 11, 5)) == (5, "September 3, 2017")
    assert calculate_age_and_birthday_week(datetime(2017, 9, 9), datetime(2022, 11, 5)) == (5, "September 3, 2017")
    
    # AC-4.3
    assert calculate_age_and_birthday_week(datetime(2017, 9, 4), datetime(2022, 11, 5)) == (5, "August 29, 2017")
    assert calculate_age_and_birthday_week(datetime(2017, 9, 6), datetime(2022, 11, 5)) == (5, "August 31, 2017")