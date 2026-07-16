# test_video_rental.py

from solution import price_rental, award_points, Customer, Movie

def test_price_regular_movie_for_two_days():
    # Regular movie costs 2.0 for up to two days
    assert price_rental('REGULAR', 2) == 2.0

def test_price_regular_movie_for_three_days():
    # Regular movie costs 2.0 for two days + 1.5 for the third day = 3.5
    assert price_rental('REGULAR', 3) == 3.5

def test_price_regular_movie_for_five_days():
    # Regular movie costs 2.0 for two days + 3 * 1.5 for the additional three days = 6.5
    assert price_rental('REGULAR', 5) == 6.5

def test_price_new_release_for_one_day():
    # New release costs 3.0 for one day
    assert price_rental('NEW_RELEASE', 1) == 3.0

def test_price_new_release_for_three_days():
    # New release costs 3.0 * 3 = 9.0
    assert price_rental('NEW_RELEASE', 3) == 9.0

def test_price_childrens_movie_for_three_days():
    # Children's movie costs 1.5 for up to three days
    assert price_rental('CHILDRENS', 3) == 1.5

def test_price_childrens_movie_for_four_days():
    # Children's movie costs 1.5 for three days + 1.5 for the fourth day = 3.0
    assert price_rental('CHILDRENS', 4) == 3.0

def test_price_childrens_movie_for_six_days():
    # Children's movie costs 1.5 for three days + 3 * 1.5 for the additional three days = 6.0
    assert price_rental('CHILDRENS', 6) == 6.0

def test_price_rental_rejects_zero_days():
    # Rental must last at least one day
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        price_rental('REGULAR', 0)

def test_price_rental_rejects_negative_days():
    # Rental must last at least one day
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        price_rental('REGULAR', -1)

def test_award_points_for_regular_movie():
    # Every rental earns one point
    assert award_points('REGULAR', 1) == 1

def test_award_points_for_new_release_one_day():
    # New release earns one point
    assert award_points('NEW_RELEASE', 1) == 1

def test_award_points_for_new_release_two_days():
    # New release earns one bonus point for being rented more than one day
    assert award_points('NEW_RELEASE', 2) == 2

def test_award_points_for_new_release_three_days():
    # New release earns one bonus point for being rented more than one day
    assert award_points('NEW_RELEASE', 3) == 2

def test_customer_total_charge_and_points():
    customer = Customer("John Doe")
    customer.add_rental(Movie("Regular Movie", 'REGULAR'), 3)  # 3.5 charge, 1 point
    customer.add_rental(Movie("New Release Movie", 'NEW_RELEASE'), 2)  # 6.0 charge, 2 points
    customer.add_rental(Movie("Children's Movie", 'CHILDRENS'), 4)  # 3.0 charge, 1 point
    # Total charge = 3.5 + 6.0 + 3.0 = 12.5, Total points = 1 + 2 + 1 = 4
    assert customer.total_charge() == 12.5
    assert customer.total_points() == 4

def test_customer_statement_with_rentals():
    customer = Customer("Jane Doe")
    customer.add_rental(Movie("Regular Movie", 'REGULAR'), 3)
    statement = customer.statement()
    expected_statement = (
        "Rental Record for Jane Doe\n"
        "\tRegular Movie\t3.5\n"
        "Amount owed is 3.5\n"
        "You earned 1 frequent renter points"
    )
    assert statement == expected_statement

def test_customer_statement_with_no_rentals():
    customer = Customer("John Smith")
    statement = customer.statement()
    expected_statement = (
        "Rental Record for John Smith\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert statement == expected_statement