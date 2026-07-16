# candidate/impl.py

from datetime import datetime, timedelta

class BirthdayService:
    def __init__(self, birthdate: str, reference_date: str):
        self.birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        self.reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
        self._validate_dates()

    def _validate_dates(self):
        if self.birthdate > self.reference_date:
            raise ValueError("birthdate is after today")

    def age_in_years(self) -> int:
        """Calculate age in completed years."""
        age = self.reference_date.year - self.birthdate.year
        
        if (self.reference_date.month, self.reference_date.day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        
        # Special case for leap day birthdays
        if self.birthdate.month == 2 and self.birthdate.day == 29:
            if not self.is_leap_year(self.reference_date.year) and (self.reference_date.month, self.reference_date.day) < (3, 1):
                age -= 1
        
        return max(age, 0)

    def birthday_week_start(self) -> str:
        """Calculate the start date of the birthday week."""
        birthday = self.birthdate
        if birthday.month == 2 and birthday.day == 29:
            birthday_this_year = datetime(birthday.year + (1 if self.is_leap_year(birthday.year + 1) else 0), 3, 1)
        else:
            birthday_this_year = datetime(birthday.year, birthday.month, birthday.day)
        
        if birthday_this_year.weekday() in [3, 4, 5]:  # Thursday, Friday, Saturday
            start_date = birthday_this_year - timedelta(days=birthday_this_year.weekday() + 1)
        else:  # Sunday, Monday, Tuesday, Wednesday
            start_date = birthday_this_year - timedelta(days=(birthday_this_year.weekday() + 6) % 7)
        
        return start_date.strftime('%B %d, %Y')

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Check if a year is a leap year."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Example Usage:
# service = BirthdayService('2016-10-28', '2022-11-05')
# print(service.age_in_years())  # Outputs: 6
# print(service.birthday_week_start())  # Outputs: "October 30, 2022"
