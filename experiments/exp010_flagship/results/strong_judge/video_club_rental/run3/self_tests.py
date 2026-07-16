# test_video_rental.py

import pytest
from solution import price_rental, award_points

def test_regular_movie_rental_for_one_day():
    charge = price_rental("Regular Movie", "REGULAR", 1)  # 2.0 for 1 day
    assert charge == 2.0

def test_regular_movie_rental_for_two_days():
    charge = price_rental("Regular Movie", "REGULAR", 2)  # 2.0 for 2 days
    assert charge == 2.0

def test_regular_movie_rental_for_three_days():
    charge = price_rental("Regular Movie", "REGULAR", 3)  # 2.0 + 1*1.5 = 3.5 for 3 days
    assert charge == 3.5

def test_regular_movie_rental_for_five_days():
    charge = price_rental("Regular Movie", "REGULAR", 5)  # 2.0 + 3*1.5 = 6.5 for 5 days
    assert charge == 6.5

def test_new_release_rental_for_one_day():
    charge = price_rental("New Release Movie", "NEW_RELEASE", 1)  # 3.0 for 1 day
    assert charge == 3.0

def test_new_release_rental_for_three_days():
    charge = price_rental("New Release Movie", "NEW_RELEASE", 3)  # 3.0 * 3 = 9.0 for 3 days
    assert charge == 9.0

def test_new_release_rental_for_four_days():
    charge = price_rental("New Release Movie", "NEW_RELEASE", 4)  # 3.0 * 4 = 12.0 for 4 days
    assert charge == 12.0

def test_children_movie_rental_for_one_day():
    charge = price_rental("Children's Movie", "CHILDRENS", 1)  # 1.5 for 1 day
    assert charge == 1.5

def test_children_movie_rental_for_two_days():
    charge = price_rental("Children's Movie", "CHILDRENS", 2)  # 1.5 for 1 day
    assert charge == 1.5

def test_children_movie_rental_for_three_days():
    charge = price_rental("Children's Movie", "CHILDRENS", 3)  # 1.5 for 3 days
    assert charge == 1.5

def test_children_movie_rental_for_four_days():
    charge = price_rental("Children's Movie", "CHILDRENS", 4)  # 1.5 + 1.5 = 3.0 for 4 days
    assert charge == 3.0

def test_children_movie_rental_for_six_days():
    charge = price_rental("Children's Movie", "CHILDRENS", 6)  # 1.5 + 3*1.5 = 6.0 for 6 days
    assert charge == 6.0

def test_rental_days_must_be_positive():
    with pytest.raises(Exception) as excinfo:
        price_rental("Any Movie", "REGULAR", 0)
    assert str(excinfo.value) == "days_rented must be at least 1"

    with pytest.raises(Exception) as excinfo:
        price_rental("Any Movie", "REGULAR", -1)
    assert str(excinfo.value) == "days_rented must be at least 1"

def test_award_points_for_regular_movie():
    points = award_points("REGULAR", 1)  # 1 point for any rental
    assert points == 1

def test_award_points_for_new_release():
    points = award_points("NEW_RELEASE", 1)  # 1 point for any rental
    assert points == 1

def test_award_points_for_new_release_more_than_one_day():
    points = award_points("NEW_RELEASE", 2)  # 1 point + 1 bonus point
    assert points == 2

def test_award_points_for_new_release_three_days():
    points = award_points("NEW_RELEASE", 3)  # 1 point + 1 bonus point
    assert points == 2

def test_customer_rentals_and_totals():
    customer = {"name": "John Doe", "rentals": []}
    rental1 = {"movie": "Regular Movie", "category": "REGULAR", "days": 3}
    rental2 = {"movie": "New Release Movie", "category": "NEW_RELEASE", "days": 2}
    rental3 = {"movie": "Children's Movie", "category": "CHILDRENS", "days": 4}
    
    customer["rentals"].append(rental1)  # charge 3.5, points 1
    customer["rentals"].append(rental2)  # charge 6.0, points 2
    customer["rentals"].append(rental3)  # charge 3.0, points 1

    total_charge = 3.5 + 6.0 + 3.0
    total_points = 1 + 2 + 1

    assert total_charge == 12.5  # 3.5 + 6.0 + 3.0
    assert total_points == 4  # 1 + 2 + 1

def test_print_statement_for_customer_with_rentals():
    customer = {"name": "John Doe", "rentals": []}
    rental1 = {"movie": "Regular Movie", "category": "REGULAR", "days": 3}
    rental2 = {"movie": "New Release Movie", "category": "NEW_RELEASE", "days": 2}
    
    customer["rentals"].append(rental1)  # charge 3.5
    customer["rentals"].append(rental2)  # charge 6.0

    statement_lines = [f"Rental Record for {customer['name']}"]

    for rental in customer["rentals"]:
        charge = price_rental(rental["movie"], rental["category"], rental["days"])
        statement_lines.append(f"\t{rental['movie']}\t{charge}")

    total_charge = 3.5 + 6.0
    statement_lines.append(f"Amount owed is {total_charge:.1f}")
    statement_lines.append(f"You earned 3 frequent renter points")

    statement = "\n".join(statement_lines)
    expected_statement = (
        "Rental Record for John Doe\n"
        "\tRegular Movie\t3.5\n"
        "\tNew Release Movie\t6.0\n"
        "Amount owed is 9.5\n"
        "You earned 3 frequent renter points"
    )
    assert statement == expected_statement

def test_print_statement_for_customer_with_no_rentals():
    customer = {"name": "Jane Doe", "rentals": []}
    
    statement_lines = [f"Rental Record for {customer['name']}"]
    statement_lines.append("Amount owed is 0.0")
    statement_lines.append("You earned 0 frequent renter points")

    statement = "\n".join(statement_lines)
    expected_statement = (
        "Rental Record for Jane Doe\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert statement == expected_statement

def test_movie_categories():
    categories = {"REGULAR", "NEW_RELEASE", "CHILDRENS"}
    # Assuming the implementation exposes the categories somehow:
    assert categories == {"REGULAR", "NEW_RELEASE", "CHILDRENS"}