from solution import calculate_age_and_birthday_week
import pytest
from datetime import datetime

def test_age_completed_years():
    # AC-1.1: Born 28 October 2016, referenced 5 November 2022
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2022, 11, 5)) == (6, "October 23, 2016")
    
    # AC-1.2: Born 31 December, referenced 1 January next year
    assert calculate_age_and_birthday_week(datetime(2016, 12, 31), datetime(2017, 1, 1)) == (0, "December 25, 2016")
    
    # AC-1.3: Born 28 October 2016, referenced 28 October 2022 (anniversary)
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2022, 10, 28)) == (6, "October 23, 2016")
    
    # AC-1.4: Birth date equals reference date
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2016, 10, 28)) == (0, "October 23, 2016")

    # AC-1.2: Before first anniversary
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2016, 10, 27)) == (0, "October 23, 2016")

    # AC-1.2: Day before later anniversary
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2022, 10, 27)) == (5, "October 23, 2016")

    # AC-1.3: Day after anniversary
    assert calculate_age_and_birthday_week(datetime(2016, 10, 28), datetime(2022, 10, 29)) == (6, "October 23, 2016")

def test_leap_day_birthdays():
    # AC-2.1: Born 29 February, referenced 1 March (non-leap year)
    assert calculate_age_and_birthday_week(datetime(2000, 2, 29), datetime(2021, 3, 1)) == (21, "February 28, 2021")
    
    # AC-2.2: Born 29 February, referenced 29 February (leap year)
    assert calculate_age_and_birthday_week(datetime(2000, 2, 29), datetime(2020, 2, 29)) == (20, "February 23, 2020")

    # AC-2.1: Born 29 February, referenced 28 February (non-leap year)
    assert calculate_age_and_birthday_week(datetime(2000, 2, 29), datetime(2021, 2, 28)) == (21, "February 28, 2021")

def test_future_birth_dates():
    # AC-3.1: Birth date after reference date (should not raise an error)
    assert calculate_age_and_birthday_week(datetime(2024, 1, 1), datetime(2024, 1, 2)) == (0, "January 1, 2024")
    
    # AC-3.2: Birth date one day after reference date
    with pytest.raises(ValueError) as exc_info:
        calculate_age_and_birthday_week(datetime(2024, 1, 2), datetime(2024, 1, 1))
    assert str(exc_info.value) == "birthdate is after today"

def test_birthday_week_start_date():
    # AC-4.1: Birthday on 7 September 2017 (Thursday)
    assert calculate_age_and_birthday_week(datetime(2017, 9, 7), datetime(2017, 9, 7)) == (0, "September 3, 2017")
    
    # AC-4.2: Birthday on 8 September 2017 (Friday)
    assert calculate_age_and_birthday_week(datetime(2017, 9, 8), datetime(2017, 9, 8)) == (0, "September 3, 2017")
    
    # AC-4.3: Birthday on 4 September 2017 (Monday)
    assert calculate_age_and_birthday_week(datetime(2017, 9, 4), datetime(2017, 9, 4)) == (0, "August 29, 2017")

    # Additional test for Saturday (9 September 2017)
    assert calculate_age_and_birthday_week(datetime(2017, 9, 9), datetime(2017, 9, 9)) == (0, "September 3, 2017")

    # Additional test for Sunday (3 September 2017)
    assert calculate_age_and_birthday_week(datetime(2017, 9, 3), datetime(2017, 9, 3)) == (0, "August 28, 2017")

    # Additional test for Wednesday (6 September 2017)
    assert calculate_age_and_birthday_week(datetime(2017, 9, 6), datetime(2017, 9, 6)) == (0, "August 31, 2017")