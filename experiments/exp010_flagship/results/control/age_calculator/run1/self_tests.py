import pytest
from solution import calculate_age_and_birthday_week

def test_age_in_completed_years():
    # AC-1.1: born 28 October 2016, reference 5 November 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "October 28, 2022")
    
    # AC-1.2: born 31 December, referenced 1 January next year
    assert calculate_age_and_birthday_week("2016-12-31", "2017-01-01") == (0, "January 1, 2017")
    
    # AC-1.3: born 28 October, referenced 29 October
    assert calculate_age_and_birthday_week("2016-10-28", "2022-10-29") == (6, "October 28, 2022")
    
    # AC-1.4: birth date equals reference date
    assert calculate_age_and_birthday_week("2022-11-05", "2022-11-05") == (0, "November 1, 2022")

def test_leap_day_birthdays():
    # AC-2.1: born 29 February, reference 28 February (non-leap year)
    assert calculate_age_and_birthday_week("2016-02-29", "2022-02-28") == (5, "March 1, 2022")
    
    # AC-2.2: born 29 February, reference 29 February (leap year)
    assert calculate_age_and_birthday_week("2016-02-29", "2020-02-29") == (4, "February 29, 2020")

def test_future_birth_dates_rejected():
    # AC-3.1: birthdate after reference date
    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age_and_birthday_week("2023-10-01", "2023-09-30")
    
    # AC-3.2: birthdate one day after reference date
    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age_and_birthday_week("2023-10-01", "2023-10-01")

def test_birthday_week_start_dates():
    # AC-4.1: birthday on 7 September 2017 (Thursday)
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-07") == (0, "September 3, 2017")
    
    # AC-4.2: birthday on 4 September 2017 (Monday)
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")
    
    # AC-4.3: birthday on 6 September 2017 (Wednesday)
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")