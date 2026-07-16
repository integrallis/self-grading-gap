import pytest
from solution import calculate_age_and_birthday_week

def test_age_in_completed_years():
    # AC-1.1
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "November 1, 2022")
    
    # AC-1.2
    assert calculate_age_and_birthday_week("2016-12-31", "2017-01-01") == (0, "December 31, 2017")
    
    # AC-1.3
    assert calculate_age_and_birthday_week("2016-10-28", "2017-10-28") == (1, "October 22, 2017")  # Age increments to 1 on the anniversary
    
    # AC-1.4
    assert calculate_age_and_birthday_week("2022-11-05", "2022-11-05") == (0, "November 1, 2022")

def test_leap_day_birthdays():
    # AC-2.1
    assert calculate_age_and_birthday_week("2000-02-29", "2021-02-28") == (20, "February 28, 2021")  # Age remains 20 as 29 Feb hasn't occurred yet this year
    
    # AC-2.2
    assert calculate_age_and_birthday_week("2000-02-29", "2020-02-29") == (20, "February 23, 2020")  # Age increments on 29 Feb itself

def test_future_birth_dates():
    # AC-3.1
    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age_and_birthday_week("2023-10-01", "2023-09-30")
    
    # AC-3.2
    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age_and_birthday_week("2023-09-30", "2023-09-29")

def test_birthday_week_start_date():
    # AC-4.1
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-07") == (0, "September 3, 2017")  # Thursday
    
    assert calculate_age_and_birthday_week("2017-09-08", "2017-09-08") == (0, "September 3, 2017")  # Friday
    
    assert calculate_age_and_birthday_week("2017-09-09", "2017-09-09") == (0, "September 3, 2017")  # Saturday
    
    # AC-4.3
    assert calculate_age_and_birthday_week("2017-09-03", "2017-09-03") == (0, "August 28, 2017")  # Sunday
    
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")  # Monday
    
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")  # Wednesday