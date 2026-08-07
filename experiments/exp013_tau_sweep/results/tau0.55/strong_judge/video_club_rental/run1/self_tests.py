# test_video_rental.py

import pytest
from solution import price_rental, award_points, Movie, PricingCategory, Customer, print_statement

def test_price_rental_regular_movie():
    # Regular movie costs 2.0 for up to 2 days, plus 1.5 for each day beyond the second
    assert price_rental(PricingCategory.REGULAR, 1) == 2.0  # 2.0
    assert price_rental(PricingCategory.REGULAR, 2) == 2.0  # 2.0
    assert price_rental(PricingCategory.REGULAR, 3) == 3.5  # 2.0 + 1.5
    assert price_rental(PricingCategory.REGULAR, 5) == 6.5  # 2.0 + 1.5 * 3

def test_price_rental_new_release():
    # New release costs 3.0 per day rented
    assert price_rental(PricingCategory.NEW_RELEASE, 1) == 3.0  # 3.0
    assert price_rental(PricingCategory.NEW_RELEASE, 3) == 9.0  # 3.0 * 3

def test_price_rental_childrens_movie():
    # Children's movie costs 1.5 for up to 3 days, plus 1.5 for each day beyond the third
    assert price_rental(PricingCategory.CHILDRENS, 1) == 1.5  # 1.5
    assert price_rental(PricingCategory.CHILDRENS, 3) == 1.5  # 1.5
    assert price_rental(PricingCategory.CHILDRENS, 4) == 3.0  # 1.5 + 1.5
    assert price_rental(PricingCategory.CHILDRENS, 6) == 6.0  # 1.5 + 1.5 * 3

def test_price_rental_invalid_days():
    # Rental must last at least one day
    with pytest.raises(Exception, match="days_rented must be at least 1"):
        price_rental(PricingCategory.REGULAR, 0)
    with pytest.raises(Exception, match="days_rented must be at least 1"):
        price_rental(PricingCategory.REGULAR, -1)

def test_award_points_regular_movie():
    # Every rental earns one frequent renter point
    assert award_points(PricingCategory.REGULAR, 1) == 1  # 1 point
    assert award_points(PricingCategory.REGULAR, 3) == 1  # 1 point

def test_award_points_childrens_movie():
    # Every rental earns one frequent renter point
    assert award_points(PricingCategory.CHILDRENS, 1) == 1  # 1 point
    assert award_points(PricingCategory.CHILDRENS, 2) == 1  # 1 point

def test_award_points_new_release():
    # New release kept more than one day earns one bonus point
    assert award_points(PricingCategory.NEW_RELEASE, 1) == 1  # 1 point
    assert award_points(PricingCategory.NEW_RELEASE, 2) == 2  # 1 point + 1 bonus point
    assert award_points(PricingCategory.NEW_RELEASE, 3) == 2  # 1 point + 1 bonus point
    assert award_points(PricingCategory.NEW_RELEASE, 4) == 2  # 1 point + 1 bonus point

def test_movie_exposes_title_and_category():
    movie = Movie("Inception", PricingCategory.NEW_RELEASE)
    assert movie.title == "Inception"
    assert movie.category == PricingCategory.NEW_RELEASE

def test_pricing_categories_count():
    categories = {PricingCategory.REGULAR, PricingCategory.NEW_RELEASE, PricingCategory.CHILDRENS}
    assert len(categories) == 3  # Ensure there are exactly three categories
    assert PricingCategory.REGULAR in categories
    assert PricingCategory.NEW_RELEASE in categories
    assert PricingCategory.CHILDRENS in categories

def test_customer_account():
    customer = Customer("John Doe")
    customer.add_rental(Movie("Movie 1", PricingCategory.REGULAR), 3)  # 3.5 charge
    customer.add_rental(Movie("Movie 2", PricingCategory.NEW_RELEASE), 2)  # 6.0 charge
    customer.add_rental(Movie("Movie 3", PricingCategory.CHILDRENS), 4)  # 3.0 charge

    assert customer.total_charge() == 12.5  # 3.5 + 6.0 + 3.0
    assert customer.total_points() == 4  # 1 + 2 + 1

def test_print_statement_no_rentals():
    # Customer with no rentals
    assert print_statement("Jane Doe", []) == (
        "Rental Record for Jane Doe\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )

def test_print_statement_with_rentals():
    # Customer with rentals
    rentals = [
        (Movie("Movie 1", PricingCategory.REGULAR), 3),  # 3.5
        (Movie("Movie 2", PricingCategory.NEW_RELEASE), 2),  # 6.0
        (Movie("Movie 3", PricingCategory.CHILDRENS), 4),  # 3.0
    ]
    
    total_charge = sum(price_rental(movie.category, days) for movie, days in rentals)  # 3.5 + 6.0 + 3.0 = 12.5
    total_points = (
        award_points(PricingCategory.REGULAR, 3) +
        award_points(PricingCategory.NEW_RELEASE, 2) +
        award_points(PricingCategory.CHILDRENS, 4)
    )  # 1 + 2 + 1 = 4 points
    
    assert print_statement("John Doe", rentals) == (
        "Rental Record for John Doe\n"
        "\tMovie 1\t3.5\n"
        "\tMovie 2\t6.0\n"
        "\tMovie 3\t3.0\n"
        f"Amount owed is {total_charge:.1f}\n"
        f"You earned {total_points} frequent renter points"
    )