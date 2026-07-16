# candidate/impl.py

from datetime import datetime, timedelta

class BirthdayService:
    def __init__(self, birth_date_str, reference_date_str):
        self.birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        self.reference_date = datetime.strptime(reference_date_str, "%Y-%m-%d")
        self.validate_dates()

    def validate_dates(self):
        if self.birth_date > self.reference_date:
            raise ValueError("birthdate is after today")

    def calculate_age(self):
        age = self.reference_date.year - self.birth_date.year
        if (self.reference_date.month, self.reference_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def birthday_week_start(self):
        birthday_this_year = datetime(self.reference_date.year, self.birth_date.month, self.birth_date.day)
        
        if birthday_this_year < self.reference_date:
            birthday_this_year = birthday_this_year.replace(year=self.reference_date.year + 1)

        if birthday_this_year.month == 2 and birthday_this_year.day == 29:
            if not self.is_leap_year(birthday_this_year.year):
                birthday_this_year = datetime(birthday_this_year.year, 3, 1)

        weekday = birthday_this_year.weekday()
        if weekday in [3, 4, 5]:  # Thursday, Friday, Saturday
            start_date = birthday_this_year - timedelta(days=weekday + 1)
        else:  # Sunday, Monday, Tuesday, Wednesday
            start_date = birthday_this_year - timedelta(days=(weekday + 6))

        return start_date.strftime("%B %d, %Y")

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Example of how to use:
# service = BirthdayService("2016-10-28", "2022-11-05")
# print(service.calculate_age())  # Output: 6
# print(service.birthday_week_start())  # Output will depend on the birth date and reference date.
