# file: video_club_rental.py
from candidate import Customer as _Customer
from candidate import Movie
from candidate import pytest


class PriceCode:
    REGULAR = "REGULAR"
    NEW_RELEASE = "NEW_RELEASE"
    CHILDRENS = "CHILDRENS"


class Rental:
    def __init__(self, movie, days_rented):
        self.movie = movie
        self.days_rented = days_rented


class Customer(_Customer):
    def add_rental(self, rental):
        return super().add_rental(rental.movie, rental.days_rented)
