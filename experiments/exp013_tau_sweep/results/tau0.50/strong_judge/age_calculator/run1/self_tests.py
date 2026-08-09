import pytest
from solution import calculate_age_and_birthday_week

def test_age_in_whole_years():
    # AC-1.1: Born 28 October 2016, reference date 5 November 2022 -> age is 6
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "October 23, 2016")
    
    # AC-1.2: Born 31 December, referenced 1 January next year -> age is 0
    assert calculate_age_and_birthday_week("2016-12-31", "2017-01-01") == (0, "January 1, 2017")
    
    # AC-1.2: Born 28 October, referenced 27 October next year -> age is 0
    assert calculate_age_and_birthday_week("2016-10-28", "2017-10-27") == (0, "October 1, 2017")
    
    # AC-1.3: Born 28 October, referenced on 28 October next year -> age is 1
    assert calculate_age_and_birthday_week("2016-10-28", "2017-10-28") == (1, "October 1, 2017")
    
    # AC-1.3: Next day after anniversary, age remains 1
    assert calculate_age_and_birthday_week("2016-10-28", "2017-10-29") == (1, "October 1, 2017")
    
    # AC-1.4: Birth date equals reference date -> age is 0
    assert calculate_age_and_birthday_week("2016-10-28", "2016-10-28") == (0, "October 23, 2016")

def test_leap_day_birthdays():
    # AC-2.1: Born on 29 February, referenced on 28 February next year -> age is 0
    assert calculate_age_and_birthday_week("2016-02-29", "2017-02-28") == (0, "February 26, 2017")
    
    # AC-2.1: Born on 29 February, referenced on 1 March next year -> age is 1
    assert calculate_age_and_birthday_week("2016-02-29", "2017-03-01") == (1, "February 26, 2017")
    
    # AC-2.2: Born on 29 February, referenced on 29 February in leap year -> age is 4
    assert calculate_age_and_birthday_week("2016-02-29", "2020-02-29") == (4, "February 23, 2020")

def test_future_birth_dates():
    # AC-3.1: Birth date after reference date -> error
    with pytest.raises(Exception) as exc_info:
        calculate_age_and_birthday_week("2023-10-28", "2023-10-27")
    assert str(exc_info.value) == "birthdate is after today"
    
    # AC-3.2: Birth date equal to reference date -> should not raise error and age is 0
    assert calculate_age_and_birthday_week("2023-10-28", "2023-10-28") == (0, "October 23, 2023")

def test_birthday_week_start_date():
    # AC-4.1: Birthday on 7 September 2017 -> week starts on 3 September 2017
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-07") == (0, "September 3, 2017")
    
    # AC-4.2: Birthday on 29 September 2017 -> week starts on 24 September 2017
    assert calculate_age_and_birthday_week("2017-09-29", "2017-09-29") == (0, "September 24, 2017")

    # AC-4.2: Birthday on 9 September 2017 -> week starts on 3 September 2017
    assert calculate_age_and_birthday_week("2017-09-09", "2017-09-09") == (0, "September 3, 2017")

    # AC-4.3: Birthday on 3 September 2017 -> week starts on 28 August 2017
    assert calculate_age_and_birthday_week("2017-09-03", "2017-09-03") == (0, "August 28, 2017")
    
    # AC-4.3: Birthday on 4 September 2017 -> week starts on 29 August 2017
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")
    
    # AC-4.3: Birthday on 6 September 2017 -> week starts on 31 August 2017
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")