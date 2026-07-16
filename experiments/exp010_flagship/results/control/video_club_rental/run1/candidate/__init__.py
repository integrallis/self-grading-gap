import pytest

def price_rental(movie_type, days_rented):
    if days_rented < 1:
        raise ValueError("days_rented must be at least 1")
    if movie_type == 'REGULAR':
        price = 2.0
        if days_rented > 2:
            price += (days_rented - 2) * 1.5
    elif movie_type == 'NEW_RELEASE':
        price = 3.0 * days_rented
    elif movie_type == 'CHILDRENS':
        price = 1.5
        if days_rented > 3:
            price += (days_rented - 3) * 1.5
    else:
        raise ValueError("Invalid movie type")
    return price

def award_points(movie_type, days_rented):
    if movie_type == 'NEW_RELEASE' and days_rented > 1:
        return 2
    return 1

class Movie:
    def __init__(self, title, movie_type):
        self.title = title
        self.movie_type = movie_type

class Customer:
    def __init__(self, name):
        self.name = name
        self.rentals = []

    def add_rental(self, movie, days_rented):
        self.rentals.append((movie, days_rented))

    def total_charge(self):
        return sum(price_rental(movie.movie_type, days) for movie, days in self.rentals)

    def total_points(self):
        return sum(award_points(movie.movie_type, days) for movie, days in self.rentals)

    def statement(self):
        result = f"Rental Record for {self.name}\n"
        for movie, days in self.rentals:
            result += f"\t{movie.title}\t{price_rental(movie.movie_type, days):.1f}\n"
        result += f"Amount owed is {self.total_charge():.1f}\n"
        result += f"You earned {self.total_points()} frequent renter points"
        return result