from solution import last_sundays
import pytest

def test_last_sundays_2013():
    # Expected: 2013-01-27, 2013-02-24, 2013-03-31, 2013-04-28, 2013-05-26,
    # 2013-06-30, 2013-07-28, 2013-08-25, 2013-09-29, 2013-10-27, 2013-11-24, 2013-12-29
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28",
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25",
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert last_sundays(2013) == expected

def test_last_sundays_2032():
    # Expected: 2032-01-25, 2032-02-29, 2032-03-28, 2032-04-25,
    # 2032-05-30, 2032-06-27, 2032-07-25, 2032-08-29, 2032-09-26,
    # 2032-10-31, 2032-11-28, 2032-12-26
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25",
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29",
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert last_sundays(2032) == expected

def test_last_sundays_2024():
    # Expected: 2024-01-28, 2024-02-25, 2024-03-31, 2024-04-28,
    # 2024-05-26, 2024-06-30, 2024-07-28, 2024-08-25, 2024-09-29,
    # 2024-10-27, 2024-11-24, 2024-12-29
    expected = [
        "2024-01-28", "2024-02-25", "2024-03-31", "2024-04-28",
        "2024-05-26", "2024-06-30", "2024-07-28", "2024-08-25",
        "2024-09-29", "2024-10-27", "2024-11-24", "2024-12-29"
    ]
    assert last_sundays(2024) == expected

def test_last_sundays_2100():
    # Expected: 2100-01-31, 2100-02-28, 2100-03-28, 2100-04-25,
    # 2100-05-30, 2100-06-27, 2100-07-25, 2100-08-29, 2100-09-26,
    # 2100-10-31, 2100-11-28, 2100-12-26
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25",
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29",
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert last_sundays(2100) == expected

def test_last_sunday_of_month_january_2013():
    # Expected: 2013-01-27
    assert last_sundays(2013, 1) == "2013-01-27"

def test_last_sunday_of_month_february_2013():
    # Expected: 2013-02-24
    assert last_sundays(2013, 2) == "2013-02-24"

def test_last_sunday_of_month_march_2013():
    # Expected: 2013-03-31
    assert last_sundays(2013, 3) == "2013-03-31"

def test_last_sunday_of_month_february_2024():
    # Expected: 2024-02-25
    assert last_sundays(2024, 2) == "2024-02-25"

def test_last_sunday_of_month_february_2032():
    # Expected: 2032-02-29
    assert last_sundays(2032, 2) == "2032-02-29"

def test_last_sunday_of_month_invalid_month():
    # Expected: ValueError with message "month must be in 1..12"
    with pytest.raises(ValueError, match="^month must be in 1\\.\\.12$"):
        last_sundays(2013, 13)

def test_last_sunday_of_month_invalid_negative_month():
    # Expected: ValueError with message "month must be in 1..12"
    with pytest.raises(ValueError, match="^month must be in 1\\.\\.12$"):
        last_sundays(2013, 0)

def test_last_sunday_of_month_december_2000():
    # Expected: 2000-12-31
    assert last_sundays(2000, 12) == "2000-12-31"

def test_last_sundays_december_entry_2000():
    # Expected: 2000-12-31
    assert last_sundays(2000)[11] == "2000-12-31"