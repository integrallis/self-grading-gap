import pytest
from solution import TransitCard

def test_journey_within_zone_a():
    card = TransitCard()
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # AC-1.1
    assert charge == 2.50  # Journey wholly within Zone A

def test_journey_within_zone_b():
    card = TransitCard()
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # AC-1.2
    assert charge == 3.00  # Journey wholly within Zone B

def test_journey_touching_zone_b():
    card = TransitCard()
    charge = card.journey("Aldgate", "Balham", "2023-10-01")  # AC-1.3
    assert charge == 3.00  # Journey touching Zone B

def test_journey_unknown_station():
    card = TransitCard()
    with pytest.raises(Exception) as excinfo:  # Catch unspecified unknown-station error
        card.journey("Aldgate", "UnknownStation", "2023-10-01")  # AC-4.1
    assert "UnknownStation" in str(excinfo.value)  # Journey involving unknown station

def test_journey_charge_unknown_station():
    card = TransitCard()
    with pytest.raises(Exception):  # Journey should be rejected
        card.journey("Aldgate", "UnknownStation", "2023-10-01")  # AC-4.1
    assert card.get_total() == 0.00  # AC-4.2

def test_daily_cap_zone_a():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    assert charge == 2.00  # AC-2.1

def test_daily_cap_zone_a_fourth_journey_zero_charge():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # 0.00
    assert charge == 0.00  # Fourth journey capped at 7.00

def test_daily_cap_zone_b():
    card = TransitCard()
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # 2.00
    assert charge == 2.00  # AC-2.2

def test_daily_cap_zone_b_fourth_journey_zero_charge():
    card = TransitCard()
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    card.journey("Balham", "Barbican", "2023-10-01")  # 2.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # 0.00
    assert charge == 0.00  # Fourth journey capped at 8.00

def test_daily_cap_zone_b_after_zone_a():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # AC-2.4
    assert charge == 1.00  # Difference lifted to Zone B limit

def test_next_day_charge_full_fare():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-02")  # Full fare next day
    assert charge == 2.50  # AC-2.3

def test_weekly_cap_zone_a():
    card = TransitCard()
    dates = ["2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06", "2023-10-07"]  # ISO week 40
    for date in dates:
        card.journey("Aldgate", "Anerley", date)  # 3 journeys each day
        card.journey("Aldgate", "Anerley", date)  # 3 journeys each day
        card.journey("Aldgate", "Anerley", date)  # 3 journeys each day
    assert card.get_total() == 40.00  # AC-3.1

def test_weekly_cap_zone_a_new_week():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-02")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-03")  # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-09")  # Full fare on new week
    assert charge == 2.50  # AC-3.2

def test_monthly_cap_zone_a():
    card = TransitCard()
    for day in range(1, 32):  # 3 journeys every day for 31 days
        card.journey("Aldgate", "Anerley", f"2023-10-{day:02d}")
        card.journey("Aldgate", "Anerley", f"2023-10-{day:02d}")
        card.journey("Aldgate", "Anerley", f"2023-10-{day:02d}")
    assert card.get_total() == 145.00  # AC-3.3

def test_total_accumulated():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    assert card.get_total() == 5.50  # AC-5.1

def test_journey_with_amersham():
    card = TransitCard()
    charge = card.journey("Aldgate", "Amersham", "2023-10-01")  # AC-1.3
    assert charge == 2.50  # Journey touching Zone A

def test_journey_with_angel():
    card = TransitCard()
    charge = card.journey("Angel", "Anerley", "2023-10-01")  # AC-1.3
    assert charge == 2.50  # Journey touching Zone A

def test_journey_with_asterisk():
    card = TransitCard()
    charge = card.journey("Asterisk", "Anerley", "2023-10-01")  # AC-1.3
    assert charge == 2.50  # Journey touching Zone A

def test_journey_with_bison():
    card = TransitCard()
    charge = card.journey("Bison", "Balham", "2023-10-01")  # AC-1.3
    assert charge == 3.00  # Journey touching Zone B

def test_journey_with_bugel():
    card = TransitCard()
    charge = card.journey("Bugel", "Balham", "2023-10-01")  # AC-1.3
    assert charge == 3.00  # Journey touching Zone B

def test_journey_with_bullhead():
    card = TransitCard()
    charge = card.journey("Bullhead", "Balham", "2023-10-01")  # AC-1.3
    assert charge == 3.00  # Journey touching Zone B

def test_weekly_cap_zone_b():
    card = TransitCard()
    dates = ["2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06", "2023-10-07"]  # ISO week 40
    for date in dates:
        card.journey("Balham", "Barbican", date)  # 3 journeys each day
        card.journey("Balham", "Barbican", date)  # 3 journeys each day
        card.journey("Balham", "Barbican", date)  # 3 journeys each day
    assert card.get_total() == 47.00  # AC-3.1 for Zone B

def test_monthly_cap_zone_b():
    card = TransitCard()
    for day in range(1, 32):  # 3 journeys every day for 31 days
        card.journey("Balham", "Barbican", f"2023-10-{day:02d}")
        card.journey("Balham", "Barbican", f"2023-10-{day:02d}")
        card.journey("Balham", "Barbican", f"2023-10-{day:02d}")
    assert card.get_total() == 165.00  # AC-3.3 for Zone B

def test_new_month_charge():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-31")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-31")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-31")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-11-01")  # Full fare on new month
    assert card.get_total() == 2.50  # AC-3.2, new month resets cap