# test_video_rental.py

from solution import price_rental, award_frequent_renter_points, Customer, Movie, PricingCategory

def test_price_regular_movie_for_two_days():
    # Regular movie for 2 days costs 2.0
    assert price_rental(PricingCategory.REGULAR, 2) == 2.0

def test_price_regular_movie_for_three_days():
    # Regular movie for 3 days costs 3.5 (2.0 + 1.5)
    assert price_rental(PricingCategory.REGULAR, 3) == 3.5

def test_price_regular_movie_for_five_days():
    # Regular movie for 5 days costs 6.5 (2.0 + 3 * 1.5)
    assert price_rental(PricingCategory.REGULAR, 5) == 6.5

def test_price_new_release_for_one_day():
    # New release for 1 day costs 3.0
    assert price_rental(PricingCategory.NEW_RELEASE, 1) == 3.0

def test_price_new_release_for_three_days():
    # New release for 3 days costs 9.0 (3.0 * 3)
    assert price_rental(PricingCategory.NEW_RELEASE, 3) == 9.0

def test_price_children_movie_for_three_days():
    # Children's movie for 3 days costs 1.5
    assert price_rental(PricingCategory.CHILDRENS, 3) == 1.5

def test_price_children_movie_for_four_days():
    # Children's movie for 4 days costs 3.0 (1.5 + 1.5)
    assert price_rental(PricingCategory.CHILDRENS, 4) == 3.0

def test_price_children_movie_for_six_days():
    # Children's movie for 6 days costs 6.0 (1.5 + 3 * 1.5)
    assert price_rental(PricingCategory.CHILDRENS, 6) == 6.0

def test_price_rental_zero_days():
    # Rental of 0 days raises an error
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        price_rental(PricingCategory.REGULAR, 0)

def test_price_rental_negative_days():
    # Rental of negative days raises an error
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        price_rental(PricingCategory.REGULAR, -1)

def test_award_points_for_regular_movie():
    # Regular movie earns 1 point
    assert award_frequent_renter_points(PricingCategory.REGULAR, 1) == 1

def test_award_points_for_new_release_one_day():
    # New release for 1 day earns 1 point
    assert award_frequent_renter_points(PricingCategory.NEW_RELEASE, 1) == 1

def test_award_points_for_new_release_two_days():
    # New release for 2 days earns 2 points (1 base + 1 bonus)
    assert award_frequent_renter_points(PricingCategory.NEW_RELEASE, 2) == 2

def test_award_points_for_children_movie():
    # Children's movie earns 1 point
    assert award_frequent_renter_points(PricingCategory.CHILDRENS, 1) == 1

def test_customer_rental_totals():
    customer = Customer("John Doe")
    customer.add_rental(Movie("Regular Movie", PricingCategory.REGULAR), 3)  # 3.5
    customer.add_rental(Movie("New Release", PricingCategory.NEW_RELEASE), 2)  # 6.0
    customer.add_rental(Movie("Children's Movie", PricingCategory.CHILDRENS), 4)  # 3.0
    # Total charge is 3.5 + 6.0 + 3.0 = 12.5
    assert customer.total_charge() == 12.5
    # Total points are 1 + 2 + 1 = 4
    assert customer.total_points() == 4

def test_customer_statement_no_rentals():
    customer = Customer("John Doe")
    statement = customer.statement()
    assert statement == "Rental Record for John Doe\nAmount owed is 0.0\nYou earned 0 frequent renter points"

def test_customer_statement_with_rentals():
    customer = Customer("John Doe")
    customer.add_rental(Movie("Regular Movie", PricingCategory.REGULAR), 3)  # 3.5
    customer.add_rental(Movie("New Release", PricingCategory.NEW_RELEASE), 2)  # 6.0
    statement = customer.statement()
    assert statement == (
        "Rental Record for John Doe\n"
        "\tRegular Movie\t3.5\n"
        "\tNew Release\t6.0\n"
        "Amount owed is 9.5\n"
        "You earned 3 frequent renter points"
    )