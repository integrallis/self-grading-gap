import pytest
from solution import price_rental, award_frequent_renter_points, RentalAccount, print_statement, Movie, PricingCategory

# US-1: Price a rental by category and length
def test_price_regular_movie_two_days():
    assert price_rental(PricingCategory.REGULAR, 2) == 2.0  # 2.0 for up to 2 days

def test_price_regular_movie_three_days():
    assert price_rental(PricingCategory.REGULAR, 3) == 3.5  # 2.0 + 1.5 for the third day

def test_price_regular_movie_five_days():
    assert price_rental(PricingCategory.REGULAR, 5) == 6.5  # 2.0 + 3 * 1.5 for days 3, 4, 5

def test_price_new_release_one_day():
    assert price_rental(PricingCategory.NEW_RELEASE, 1) == 3.0  # 3.0 for one day

def test_price_new_release_three_days():
    assert price_rental(PricingCategory.NEW_RELEASE, 3) == 9.0  # 3.0 * 3 for three days

def test_price_children_movie_three_days():
    assert price_rental(PricingCategory.CHILDRENS, 3) == 1.5  # 1.5 for up to 3 days

def test_price_children_movie_four_days():
    assert price_rental(PricingCategory.CHILDRENS, 4) == 3.0  # 1.5 + 1.5 for the fourth day

def test_price_children_movie_six_days():
    assert price_rental(PricingCategory.CHILDRENS, 6) == 6.0  # 1.5 + 3 * 1.5 for days 4, 5, 6

def test_price_rental_zero_days():
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        price_rental(PricingCategory.REGULAR, 0)

def test_price_rental_negative_days():
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        price_rental(PricingCategory.REGULAR, -1)

# US-2: Award frequent renter points
def test_award_frequent_renter_points_regular_movie():
    assert award_frequent_renter_points(PricingCategory.REGULAR, 1) == 1  # 1 point for any rental

def test_award_frequent_renter_points_new_release_one_day():
    assert award_frequent_renter_points(PricingCategory.NEW_RELEASE, 1) == 1  # 1 point for any rental

def test_award_frequent_renter_points_new_release_two_days():
    assert award_frequent_renter_points(PricingCategory.NEW_RELEASE, 2) == 2  # 1 point + 1 bonus for >1 day

def test_award_frequent_renter_points_children_movie():
    assert award_frequent_renter_points(PricingCategory.CHILDRENS, 1) == 1  # 1 point for any rental

# US-3: Keep a customer's rental account
def test_rental_account_totals():
    account = RentalAccount("John Doe")
    account.add_rental("Movie A", PricingCategory.REGULAR, 3)  # 3.5 charge, 1 point
    account.add_rental("Movie B", PricingCategory.NEW_RELEASE, 2)  # 6.0 charge, 2 points
    account.add_rental("Movie C", PricingCategory.CHILDRENS, 4)  # 3.0 charge, 1 point
    assert account.total_charge() == 12.5  # 3.5 + 6.0 + 3.0
    assert account.total_points() == 4  # 1 + 2 + 1

def test_rental_account_empty():
    account = RentalAccount("Jane Doe")
    assert account.total_charge() == 0.0  # no rentals
    assert account.total_points() == 0  # no rentals

# US-4: Print a rental statement
def test_print_statement():
    account = RentalAccount("John Doe")
    account.add_rental("Movie A", PricingCategory.REGULAR, 3)
    account.add_rental("Movie B", PricingCategory.NEW_RELEASE, 2)
    statement = print_statement(account)
    assert statement.startswith("Rental Record for John Doe")
    assert "Movie A" in statement
    assert "Movie B" in statement
    assert "Amount owed is 12.5" in statement
    assert "You earned 4 frequent renter points" in statement

def test_print_statement_empty():
    account = RentalAccount("Jane Doe")
    statement = print_statement(account)
    assert statement == "Rental Record for Jane Doe\nAmount owed is 0.0\nYou earned 0 frequent renter points"