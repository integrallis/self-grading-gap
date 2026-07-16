from datetime import datetime, timedelta

def calculate_age_and_birthday_week(birthdate: str, reference_date: str) -> (int, str):
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
    ref_date = datetime.strptime(reference_date, "%Y-%m-%d")

    if birth_date >= ref_date:
        raise ValueError("birthdate is after today")

    # Calculate age in completed years
    age = ref_date.year - birth_date.year
    if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    # Determine the birthday week start date
    if (birth_date.month == 2 and birth_date.day == 29):
        birthday_this_year = datetime(ref_date.year, 3, 1) if is_leap_year(ref_date.year) else datetime(ref_date.year + 1, 2, 28)
    else:
        birthday_this_year = datetime(ref_date.year, birth_date.month, birth_date.day)

    week_start_date = birthday_this_year - timedelta(days=birthday_this_year.weekday())
    birthday_week_start_str = week_start_date.strftime("%B %-d, %Y")

    return age, birthday_week_start_str

def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)