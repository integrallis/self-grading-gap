from solution import TransitCard

def test_zone_a_wholly_journey_charge():
    card = TransitCard()
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")
    assert charge == 2.50  # Journey within Zone A

def test_zone_b_wholly_journey_charge():
    card = TransitCard()
    charge = card.journey("Balham", "Barbican", "2023-10-01")
    assert charge == 3.00  # Journey within Zone B

def test_zone_a_to_zone_b_journey_charge():
    card = TransitCard()
    charge = card.journey("Aldgate", "Balham", "2023-10-01")
    assert charge == 3.00  # Journey touching Zone B

def test_zone_b_to_zone_a_journey_charge():
    card = TransitCard()
    charge = card.journey("Balham", "Aldgate", "2023-10-01")
    assert charge == 3.00  # Journey touching Zone B

def test_daily_cap_zone_a():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # Should charge 2.00 to reach the cap
    assert charge == 2.00  # Total should be capped at 7.00

def test_daily_cap_zone_b():
    card = TransitCard()
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # Should charge 2.00 to reach the cap
    assert charge == 2.00  # Total should be capped at 8.00

def test_daily_cap_zone_a_with_zone_b():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00 (now at cap, charge remaining)
    charge = card.journey("Aldgate", "Balham", "2023-10-01")  # Should charge 1.00 to reach Zone B cap
    assert charge == 1.00  # Total should be capped at 8.00 for Zone B

def test_weekly_cap_zone_a():
    card = TransitCard()
    for _ in range(3):  # Three journeys for six days
        card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
        card.journey("Aldgate", "Anerley", "2023-10-02")  # 2.50
        card.journey("Aldgate", "Anerley", "2023-10-03")  # 2.50
    assert card.total() == 40.00  # Total should be capped at 40.00 for the week

def test_monthly_cap_zone_a():
    card = TransitCard()
    for day in range(1, 31):  # Three journeys every day of the month
        for _ in range(3):
            card.journey("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.50
    assert card.total() == 145.00  # Total should be capped at 145.00 for the month

def test_unknown_station_rejection():
    card = TransitCard()
    charge = card.journey("Unknown", "Anerley", "2023-10-01")
    assert charge == 0.00  # No charge for unknown station
    assert card.total() == 0.00  # Total should remain unchanged