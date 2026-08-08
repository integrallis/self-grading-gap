import pytest
from solution import calculate_age_and_birthday_week

def test_age_in_completed_years():
    # AC-1.1: Born 28 October 2016, referenced on 5 November 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "November 1, 2022")
    
    # AC-1.2: Born 31 December 2021, referenced on 1 January 2022
    assert calculate_age_and_birthday_week("2021-12-31", "2022-01-01") == (0, "January 1, 2022")
    
    # AC-1.2: Born 28 October 2016, referenced on 27 October 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-10-27") == (5, "October 30, 2022")
    
    # AC-1.3: Born 1 January 2000, referenced on 2 January 2001
    assert calculate_age_and_birthday_week("2000-01-01", "2001-01-02") == (1, "January 1, 2001")
    
    # AC-1.4: Born 15 August 2022, referenced on 15 August 2022
    assert calculate_age_and_birthday_week("2022-08-15", "2022-08-15") == (0, "August 15, 2022")
    
    # AC-1.4: Born 28 October 2016, referenced on 28 October 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-10-28") == (6, "October 30, 2022")

def test_leap_day_birthdays():
    # AC-2.1: Born 29 February 2000, referenced on 28 February 2021
    assert calculate_age_and_birthday_week("2000-02-29", "2021-02-28") == (20, "February 28, 2021")

    # AC-2.1: Born 29 February 2000, referenced on 1 March 2021
    assert calculate_age_and_birthday_week("2000-02-29", "2021-03-01") == (21, "February 28, 2021")

    # AC-2.2: Born 29 February 2000, referenced on 29 February 2024
    assert calculate_age_and_birthday_week("2000-02-29", "2024-02-29") == (24, "February 25, 2024")

def test_future_birth_dates():
    # AC-3.1: Birthdate after reference date
    with pytest.raises(Exception, match=r"^birthdate is after today$"):
        calculate_age_and_birthday_week("2023-01-01", "2022-12-31")
    
    # AC-3.2: Birthdate one day after reference date
    with pytest.raises(Exception, match=r"^birthdate is after today$"):
        calculate_age_and_birthday_week("2023-01-02", "2023-01-01")

def test_birthday_week_start_date():
    # AC-4.1: Birthday on 7 September 2017
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-07") == (0, "September 3, 2017")
    
    # AC-4.2: Birthday on 8 September 2017
    assert calculate_age_and_birthday_week("2017-09-08", "2017-09-08") == (0, "September 3, 2017")
    
    # AC-4.2: Birthday on 9 September 2017
    assert calculate_age_and_birthday_week("2017-09-09", "2017-09-09") == (0, "September 3, 2017")
    
    # AC-4.3: Birthday on 3 September 2017
    assert calculate_age_and_birthday_week("2017-09-03", "2017-09-03") == (0, "August 28, 2017")
    
    # AC-4.3: Birthday on 4 September 2017
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")
    
    # AC-4.3: Birthday on 6 September 2017
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")

def test_identical_dates_produce_identical_results():
    # Test identical birth and reference dates produce the same result
    result1 = calculate_age_and_birthday_week("2000-01-01", "2000-01-01")
    result2 = calculate_age_and_birthday_week("2000-01-01", "2000-01-01")
    assert result1 == result2