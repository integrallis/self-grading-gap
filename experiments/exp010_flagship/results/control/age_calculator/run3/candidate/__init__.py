from datetime import datetime, timedelta

def is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def calculate_age_and_birthday_week(birthdate: str, reference_date: str) -> tuple:
    birth_date = datetime.strptime(birthdate, '%Y-%m-%d')
    ref_date = datetime.strptime(reference_date, '%Y-%m-%d')

    # Check for future birthdate
    if birth_date > ref_date:
        raise ValueError('birthdate is after today')

    # Calculate age in completed years
    age = ref_date.year - birth_date.year
    if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    # Calculate the birthday for this year
    if birth_date.month == 2 and birth_date.day == 29:
        birthday_this_year = datetime(ref_date.year, 2, 29 if is_leap(ref_date.year) else 28)
    else:
        birthday_this_year = datetime(ref_date.year, birth_date.month, birth_date.day)

    if ref_date < birthday_this_year:
        birthday_this_year = datetime(ref_date.year - 1, birth_date.month, birth_date.day)

    week_start = birthday_this_year - timedelta(days=(birthday_this_year.weekday() + 3) % 7)
    birthday_week_start_date = week_start.strftime('%B %d, %Y')

    return age, birthday_week_start_date