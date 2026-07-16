import pytest
from solution import TransitCard

def test_zone_a_whole_journey_charge():
    card = TransitCard()
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # AC-1.1
    assert charge == 2.50  # Journey wholly in Zone A

def test_zone_b_whole_journey_charge():
    card = TransitCard()
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # AC-1.2
    assert charge == 3.00  # Journey wholly in Zone B

def test_zone_a_and_b_journey_charge():
    card = TransitCard()
    charge = card.journey("Aldgate", "Balham", "2023-10-01")  # AC-1.2
    assert charge == 3.00  # Journey touching Zone B

@pytest.mark.parametrize("start, end", [
    ("UnknownStation", "Anerley"),
    ("Aldgate", "UnknownStation")
])
def test_unknown_station_rejection(start, end):
    card = TransitCard()
    initial_total = card.total()
    with pytest.raises(Exception, match="UnknownStation"):  # AC-4.1
        card.journey(start, end, "2023-10-01")
    assert card.total() == initial_total  # AC-4.2

def test_daily_cap_zone_a():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")    # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    assert charge == 2.00  # AC-2.1
    assert card.total() == 7.00  # Total for the day

def test_daily_cap_zone_b():
    card = TransitCard()
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    card.journey("Balham", "Bison", "2023-10-01")     # 3.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # 2.00
    assert charge == 2.00  # AC-2.2
    assert card.total() == 8.00  # Total for the day

def test_daily_cap_zone_a_to_b():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")    # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # 1.00 difference
    assert charge == 1.00  # AC-2.4
    assert card.total() == 8.00  # Total for the day

def test_fourth_daily_zone_a_journey_charges_zero():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")    # 2.50
    charge = card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    charge = card.journey("Aldgate", "Angel", "2023-10-01")  # 0.00
    assert charge == 0.00  # AC-2.1

def test_fourth_daily_zone_b_journey_charges_zero():
    card = TransitCard()
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    card.journey("Balham", "Barbican", "2023-10-01")     # 3.00
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 2.00
    charge = card.journey("Balham", "Barbican", "2023-10-01")  # 0.00
    assert charge == 0.00  # AC-2.2

def test_daily_cap_resets_next_day():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")    # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    charge = card.journey("Aldgate", "Anerley", "2023-10-02")  # 2.50
    assert charge == 2.50  # New day charges full fare

def test_weekly_cap_zone_a():
    card = TransitCard()
    for day in range(6):  # Six days of travel
        card.journey("Aldgate", "Anerley", f"2023-10-{2 + day}")  # 2.50 each day
        card.journey("Aldgate", "Angel", f"2023-10-{2 + day}")    # 2.50 each day
    assert card.total() == 30.00  # Total for six days without reaching cap

def test_weekly_cap_zone_b():
    card = TransitCard()
    for day in range(6):  # Six days of travel
        card.journey("Balham", "Bison", f"2023-10-{2 + day}")  # 3.00 each day
        card.journey("Balham", "Barbican", f"2023-10-{2 + day}")    # 3.00 each day
    assert card.total() == 36.00  # Total for six days without reaching cap

def test_weekly_reset():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")    # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00
    card.journey("Aldgate", "Angel", "2023-10-01")    # 0.00
    card.journey("Aldgate", "Anerley", "2023-10-02")  # New week, full fare
    charge = card.journey("Aldgate", "Angel", "2023-10-02")  # 2.50
    assert charge == 2.50  # New week charges full fare

def test_monthly_cap_zone_a():
    card = TransitCard()
    for day in range(31):  # All days of October 2023
        card.journey("Aldgate", "Anerley", f"2023-10-{1 + day}")  # 2.50 each day
        card.journey("Aldgate", "Angel", f"2023-10-{1 + day}")    # 2.50 each day
    assert card.total() == 145.00  # AC-3.3

def test_monthly_cap_zone_b():
    card = TransitCard()
    for day in range(31):  # All days of October 2023
        card.journey("Balham", "Bison", f"2023-10-{1 + day}")  # 3.00 each day
        card.journey("Balham", "Barbican", f"2023-10-{1 + day}")    # 3.00 each day
    assert card.total() == 165.00  # AC-3.3

def test_calendar_month_boundary():
    card = TransitCard()
    for day in range(31):  # All days of October 2023
        card.journey("Aldgate", "Anerley", f"2023-10-{1 + day}")  # 2.50 each day
        card.journey("Aldgate", "Angel", f"2023-10-{1 + day}")    # 2.50 each day
    assert card.total() == 145.00  # Should hit the cap
    charge = card.journey("Aldgate", "Anerley", "2023-11-01")  # New month, full fare
    assert charge == 2.50  # New month charges full fare

def test_running_total_across_days():
    card = TransitCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")    # 2.50
    card.journey("Balham", "Barbican", "2023-10-02")  # 3.00
    card.journey("Balham", "Bison", "2023-10-02")     # 3.00
    assert card.total() == 11.00  # Total should reflect all journeys