from datetime import datetime, timedelta

def calculate_age_and_birthday_week(birthdate: str, reference_date: str) -> tuple:
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
    ref_date = datetime.strptime(reference_date, "%Y-%m-%d")

    if birth_date > ref_date:
        raise ValueError("birthdate is after today")

    # Calculate age in completed years
    age = ref_date.year - birth_date.year
    if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    # Calculate the birthday week start date
    if birth_date.month == 2 and birth_date.day == 29:
        # Handle leap year birthdays
        if ref_date.year < birth_date.year or (ref_date.year - birth_date.year) % 4 != 0:
            birthday_this_year = datetime(ref_date.year, 2, 28)
        else:
            birthday_this_year = datetime(ref_date.year, 2, 29)
    else:
        birthday_this_year = datetime(ref_date.year, birth_date.month, birth_date.day)

    # Determine the start of the birthday week
    if birthday_this_year == ref_date:
        birthday_week_start = birthday_this_year - timedelta(days=(birthday_this_year.weekday() + 1))
    else:
        birthday_week_start = birthday_this_year - timedelta(days=(birthday_this_year.weekday()))

    # Format the birthday week start date
    birthday_week_start_str = birthday_week_start.strftime("%B %-d, %Y")

    return (age, birthday_week_start_str) 
