# candidate/impl.py

from datetime import datetime, timedelta

class BirthdayService:
    def __init__(self, birth_date_str: str, reference_date_str: str):
        self.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        self.reference_date = datetime.strptime(reference_date_str, '%Y-%m-%d').date()
        self.validate_dates()

    def validate_dates(self):
        if self.birth_date > self.reference_date:
            raise ValueError("birthdate is after today")

    def calculate_age(self) -> int:
        age = self.reference_date.year - self.birth_date.year
        
        # Adjust age if birthday hasn't occurred yet this year
        if (self.reference_date.month, self.reference_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        
        # Special case for leap day birthdays
        if self.birth_date.month == 2 and self.birth_date.day == 29:
            if not self.is_leap_year(self.reference_date.year) and self.reference_date < datetime(self.reference_date.year, 3, 1).date():
                age -= 1
        
        return age

    def is_leap_year(self, year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def birthday_week_start(self) -> str:
        birthday = self.birth_date
        if birthday.weekday() in [3, 4, 5]:  # Thursday, Friday, Saturday
            start_date = birthday - timedelta(days=birthday.weekday() + 1)  # Go back to Sunday
        else:  # Sunday, Monday, Tuesday, Wednesday
            start_date = birthday - timedelta(days=(birthday.weekday() + 6) % 7)  # Go back to 6 days before
        
        return start_date.strftime("%B %d, %Y")

# Example usage:
# service = BirthdayService("2016-10-28", "2022-11-05")
# print(service.calculate_age())  # Outputs: 6
# print(service.birthday_week_start())  # Outputs: "October 30, 2016"
