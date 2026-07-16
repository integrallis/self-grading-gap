# candidate/impl.py

from datetime import datetime, timedelta

class BirthdayService:
    def __init__(self, birthdate: str, reference_date: str):
        self.birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        self.reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
        self.validate_dates()

    def validate_dates(self):
        if self.birthdate > self.reference_date:
            raise ValueError("birthdate is after today")

    def calculate_age(self) -> int:
        age = self.reference_date.year - self.birthdate.year
        if (self.reference_date.month, self.reference_date.day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        return age

    def birthday_week_start(self) -> str:
        birthday_this_year = self.birthdate.replace(year=self.reference_date.year)
        
        if birthday_this_year < self.reference_date:
            birthday_this_year = self.birthdate.replace(year=self.reference_date.year + 1)

        if birthday_this_year.month == 2 and birthday_this_year.day == 29:
            birthday_week_start_date = birthday_this_year
            if birthday_this_year.year % 4 != 0:  # Not a leap year
                birthday_week_start_date = birthday_this_year.replace(month=3, day=1)

        else:
            birthday_week_start_date = birthday_this_year
        
        weekday = birthday_week_start_date.weekday()  # Monday is 0
        if weekday in (5, 6):  # Saturday or Sunday
            birthday_week_start_date -= timedelta(days=weekday - 6)
        else:
            birthday_week_start_date -= timedelta(days=weekday + 1)

        return birthday_week_start_date.strftime('%B %d, %Y')

# Example usage:
# service = BirthdayService('2016-10-28', '2022-11-05')
# print(service.calculate_age())  # Output: 6
# print(service.birthday_week_start())  # Output: "October 30, 2022"
