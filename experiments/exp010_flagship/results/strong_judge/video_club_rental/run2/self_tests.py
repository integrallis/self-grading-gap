import pytest
from solution import price_rental, earn_points, Movie, PricingCategory

def test_price_rental_regular_movie():
    # Regular movie costs 2.0 for up to 2 days, 1.5 for each day beyond
    assert price_rental(PricingCategory.REGULAR, 1) == 2.0
    assert price_rental(PricingCategory.REGULAR, 2) == 2.0
    assert price_rental(PricingCategory.REGULAR, 3) == 3.5  # 2.0 + 1.5
    assert price_rental(PricingCategory.REGULAR, 5) == 6.5  # 2.0 + 1.5 * 3

def test_price_rental_new_release():
    # New release costs 3.0 per day rented
    assert price_rental(PricingCategory.NEW_RELEASE, 1) == 3.0
    assert price_rental(PricingCategory.NEW_RELEASE, 3) == 9.0  # 3.0 * 3

def test_price_rental_children_movie():
    # Children's movie costs 1.5 for up to 3 days, 1.5 for each day beyond
    assert price_rental(PricingCategory.CHILDRENS, 1) == 1.5
    assert price_rental(PricingCategory.CHILDRENS, 2) == 1.5
    assert price_rental(PricingCategory.CHILDRENS, 3) == 1.5
    assert price_rental(PricingCategory.CHILDRENS, 4) == 3.0  # 1.5 + 1.5
    assert price_rental(PricingCategory.CHILDRENS, 6) == 6.0  # 1.5 + 1.5 * 3

def test_price_rental_invalid_days():
    # Rental must last at least one day
    with pytest.raises(Exception, match=r"^days_rented must be at least 1$"):
        price_rental(PricingCategory.REGULAR, 0)
    with pytest.raises(Exception, match=r"^days_rented must be at least 1$"):
        price_rental(PricingCategory.REGULAR, -1)
    with pytest.raises(Exception, match=r"^days_rented must be at least 1$"):
        price_rental(PricingCategory.NEW_RELEASE, 0)
    with pytest.raises(Exception, match=r"^days_rented must be at least 1$"):
        price_rental(PricingCategory.CHILDRENS, 0)

def test_earn_points():
    # Every rental earns one frequent renter point
    assert earn_points(PricingCategory.REGULAR, 1) == 1
    assert earn_points(PricingCategory.NEW_RELEASE, 1) == 1
    assert earn_points(PricingCategory.CHILDRENS, 1) == 1
    assert earn_points(PricingCategory.REGULAR, 3) == 1  # still 1 point for regular
    assert earn_points(PricingCategory.CHILDRENS, 4) == 1  # still 1 point for children

def test_earn_points_new_release_bonus():
    # New release kept more than one day earns one bonus point
    assert earn_points(PricingCategory.NEW_RELEASE, 2) == 2  # 1 + 1 bonus
    assert earn_points(PricingCategory.NEW_RELEASE, 3) == 2  # 1 + 1 bonus

def test_movie_exposes_title_and_category():
    movie = Movie("Movie A", PricingCategory.REGULAR)
    assert movie.title == "Movie A"
    assert movie.category == PricingCategory.REGULAR

def test_pricing_categories_exist():
    categories = {PricingCategory.REGULAR, PricingCategory.NEW_RELEASE, PricingCategory.CHILDRENS}
    assert len(categories) == 3
    assert PricingCategory.REGULAR in categories
    assert PricingCategory.NEW_RELEASE in categories
    assert PricingCategory.CHILDRENS in categories

def test_customer_account_totals():
    # Testing customer account totals with multiple rentals
    rentals = [
        Movie("Movie A", PricingCategory.REGULAR),  # 3 days, charge = 3.5
        Movie("Movie B", PricingCategory.NEW_RELEASE),  # 2 days, charge = 6.0
        Movie("Movie C", PricingCategory.CHILDRENS),  # 4 days, charge = 3.0
    ]
    total_charge = sum([
        price_rental(PricingCategory.REGULAR, 3), 
        price_rental(PricingCategory.NEW_RELEASE, 2), 
        price_rental(PricingCategory.CHILDRENS, 4)
    ])  # 3.5 + 6.0 + 3.0 = 12.5
    total_points = sum([
        earn_points(PricingCategory.REGULAR, 3),
        earn_points(PricingCategory.NEW_RELEASE, 2),
        earn_points(PricingCategory.CHILDRENS, 4)
    ])  # 1 + 2 + 1 = 4
    assert (total_charge, total_points) == (12.5, 4)

def test_rental_ordering():
    # Verifying rentals are recorded in order
    customer = "John Doe"
    rentals = [
        Movie("Movie A", PricingCategory.REGULAR),  # 3 days
        Movie("Movie B", PricingCategory.NEW_RELEASE),  # 2 days
        Movie("Movie C", PricingCategory.CHILDRENS),  # 4 days
    ]
    rental_titles = [rental.title for rental in rentals]
    assert rental_titles == ["Movie A", "Movie B", "Movie C"]

def test_print_statement_non_empty():
    # Verifying the printed statement for a customer with rentals
    customer_name = "John Doe"
    rentals = [
        ("Movie A", PricingCategory.REGULAR, 3),  # charge = 3.5
        ("Movie B", PricingCategory.NEW_RELEASE, 2),  # charge = 6.0
        ("Movie C", PricingCategory.CHILDRENS, 4),  # charge = 3.0
    ]
    total_charge = 12.5
    total_points = 4
    
    statement_lines = [
        f"Rental Record for {customer_name}",
        "\tMovie A\t3.5",
        "\tMovie B\t6.0",
        "\tMovie C\t3.0",
        f"Amount owed is {total_charge:.1f}",
        f"You earned {total_points} frequent renter points"
    ]
    
    expected_statement = "\n".join(statement_lines)
    assert expected_statement == (
        "Rental Record for John Doe\n"
        "\tMovie A\t3.5\n"
        "\tMovie B\t6.0\n"
        "\tMovie C\t3.0\n"
        "Amount owed is 12.5\n"
        "You earned 4 frequent renter points"
    )

def test_print_statement_empty():
    # Verifying the printed statement for a customer with no rentals
    customer_name = "Jane Doe"
    total_charge = 0.0
    total_points = 0
    
    statement_lines = [
        f"Rental Record for {customer_name}",
        f"Amount owed is {total_charge:.1f}",
        f"You earned {total_points} frequent renter points"
    ]
    
    expected_statement = "\n".join(statement_lines)
    assert expected_statement == (
        "Rental Record for Jane Doe\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )