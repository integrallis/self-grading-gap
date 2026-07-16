from enum import Enum

class PricingCategory(Enum):
    REGULAR = 1
    NEW_RELEASE = 2
    CHILDRENS = 3


def price_rental(category, days_rented):
    if days_rented < 1:
        raise ValueError("days_rented must be at least 1")
    if category == PricingCategory.REGULAR:
        return 2.0 + (days_rented - 2) * 1.5 if days_rented > 2 else 2.0
    elif category == PricingCategory.NEW_RELEASE:
        return 3.0 * days_rented
    elif category == PricingCategory.CHILDRENS:
        return 1.5 + (days_rented - 3) * 1.5 if days_rented > 3 else 1.5
    raise ValueError("Invalid pricing category")


def award_frequent_renter_points(category, days_rented):
    if category == PricingCategory.NEW_RELEASE and days_rented > 1:
        return 2
    return 1

class Movie:
    def __init__(self, title, category):
        self.title = title
        self.category = category

class Customer:
    def __init__(self, name):
        self.name = name
        self.rentals = []

    def add_rental(self, movie, days_rented):
        self.rentals.append((movie, days_rented))

    def total_charge(self):
        return sum(price_rental(movie.category, days_rented) for movie, days_rented in self.rentals)

    def total_points(self):
        return sum(award_frequent_renter_points(movie.category, days_rented) for movie, days_rented in self.rentals)

    def statement(self):
        statement = f"Rental Record for {self.name}\n"
        for movie, days_rented in self.rentals:
            statement += f"\t{movie.title}\t{price_rental(movie.category, days_rented)}\n"
        statement += f"Amount owed is {self.total_charge():.1f}\n"
        statement += f"You earned {self.total_points()} frequent renter points"
        return statement
