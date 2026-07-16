import pytest
from solution import PricingCategory

def test_price_regular_movie_one_day():
    # 2.0 for first 2 days
    assert price_rental(PricingCategory.REGULAR, 1) == 2.0

def test_price_regular_movie_two_days():
    # 2.0 for first 2 days
    assert price_rental(PricingCategory.REGULAR, 2) == 2.0

def test_price_regular_movie_three_days():
    # 2.0 for first 2 days + 1.5 for the 3rd day = 3.5
    assert price_rental(PricingCategory.REGULAR, 3) == 3.5

def test_price_regular_movie_five_days():
    # 2.0 for first 2 days + 1.5 * 3 for 3 additional days = 6.5
    assert price_rental(PricingCategory.REGULAR, 5) == 6.5

def test_price_new_release_one_day():
    # 3.0 for one day
    assert price_rental(PricingCategory.NEW_RELEASE, 1) == 3.0

def test_price_new_release_three_days():
    # 3.0 * 3 for three days = 9.0
    assert price_rental(PricingCategory.NEW_RELEASE, 3) == 9.0

def test_price_childrens_movie_one_day():
    # 1.5 for first 3 days
    assert price_rental(PricingCategory.CHILDRENS, 1) == 1.5

def test_price_childrens_movie_three_days():
    # 1.5 for first 3 days
    assert price_rental(PricingCategory.CHILDRENS, 3) == 1.5

def test_price_childrens_movie_four_days():
    # 1.5 for first 3 days + 1.5 for the 4th day = 3.0
    assert price_rental(PricingCategory.CHILDRENS, 4) == 3.0

def test_price_childrens_movie_six_days():
    # 1.5 for first 3 days + 1.5 * 3 for additional 3 days = 6.0
    assert price_rental(PricingCategory.CHILDRENS, 6) == 6.0

def test_price_rental_zero_days():
    # Should raise an error with the message "days_rented must be at least 1"
    with pytest.raises(Exception, match=r"^days_rented must be at least 1$"):
        price_rental(PricingCategory.REGULAR, 0)

def test_price_rental_negative_days():
    # Should raise an error with the message "days_rented must be at least 1"
    with pytest.raises(Exception, match=r"^days_rented must be at least 1$"):
        price_rental(PricingCategory.REGULAR, -1)

def test_award_points_regular_movie():
    # 1 point for every rental
    assert award_points(PricingCategory.REGULAR, 1) == 1

def test_award_points_childrens_movie():
    # 1 point for every rental
    assert award_points(PricingCategory.CHILDRENS, 1) == 1

def test_award_points_new_release_one_day():
    # 1 point for rental
    assert award_points(PricingCategory.NEW_RELEASE, 1) == 1

def test_award_points_new_release_two_days():
    # 1 point for rental + 1 bonus point for more than 1 day
    assert award_points(PricingCategory.NEW_RELEASE, 2) == 2

def test_award_points_new_release_three_days():
    # 1 point for rental + 1 bonus point for more than 1 day
    assert award_points(PricingCategory.NEW_RELEASE, 3) == 2

def test_award_points_regular_movie_multi_day():
    # 1 point for rental regardless of length
    assert award_points(PricingCategory.REGULAR, 3) == 1

def test_award_points_childrens_movie_multi_day():
    # 1 point for rental regardless of length
    assert award_points(PricingCategory.CHILDRENS, 4) == 1

def test_accumulate_rentals():
    rentals = []
    rentals.append((Movie("Regular Movie", PricingCategory.REGULAR), 3))  # 3.5
    rentals.append((Movie("New Release", PricingCategory.NEW_RELEASE), 2))  # 6.0
    rentals.append((Movie("Children's Movie", PricingCategory.CHILDRENS), 4))  # 3.0

    total_charge, total_points = accumulate_rentals(rentals)
    
    # Total charge = 3.5 + 6.0 + 3.0 = 12.5
    # Total points = 1 + 2 + 1 = 4
    assert total_charge == 12.5
    assert total_points == 4

def test_accumulate_rentals_order():
    rentals = []
    rentals.append((Movie("First Movie", PricingCategory.REGULAR), 2))  # 2.0
    rentals.append((Movie("Second Movie", PricingCategory.NEW_RELEASE), 1))  # 3.0
    rentals.append((Movie("Third Movie", PricingCategory.CHILDRENS), 3))  # 1.5

    total_charge, total_points = accumulate_rentals(rentals)

    # Check if the rentals are in the same order
    assert rentals[0][0].title == "First Movie"
    assert rentals[1][0].title == "Second Movie"
    assert rentals[2][0].title == "Third Movie"

def test_print_statement_no_rentals():
    statement = print_statement("Customer A", [])
    expected_statement = (
        "Rental Record for Customer A\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert statement == expected_statement

def test_print_statement_with_rentals():
    rentals = [
        (Movie("Regular Movie", PricingCategory.REGULAR), 3),  # 3.5
        (Movie("New Release", PricingCategory.NEW_RELEASE), 2),  # 6.0
        (Movie("Children's Movie", PricingCategory.CHILDRENS), 4)  # 3.0
    ]
    statement = print_statement("Customer A", rentals)
    expected_statement = (
        "Rental Record for Customer A\n"
        "\tRegular Movie\t3.5\n"
        "\tNew Release\t6.0\n"
        "\tChildren's Movie\t3.0\n"
        "Amount owed is 12.5\n"
        "You earned 4 frequent renter points"
    )
    assert statement == expected_statement

def test_movie_exposes_title_and_category():
    movie = Movie("A Great Movie", PricingCategory.REGULAR)
    assert movie.title == "A Great Movie"
    assert movie.category == PricingCategory.REGULAR

def test_pricing_categories_defined():
    categories = {PricingCategory.REGULAR, PricingCategory.NEW_RELEASE, PricingCategory.CHILDRENS}
    assert len(categories) == 3
    assert PricingCategory.REGULAR in categories
    assert PricingCategory.NEW_RELEASE in categories
    assert PricingCategory.CHILDRENS in categories