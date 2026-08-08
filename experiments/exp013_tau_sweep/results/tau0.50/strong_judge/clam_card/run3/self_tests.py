import pytest
from solution import fare_card

def test_journey_within_zone_a():
    # Journey wholly within Zone A charges 2.50
    assert fare_card.charge("Aldgate", "Angel", "2023-10-01") == 2.50

def test_journey_within_zone_b():
    # Journey wholly within Zone B charges 3.00
    assert fare_card.charge("Balham", "Barbican", "2023-10-01") == 3.00

def test_journey_touching_zone_a_and_b():
    # Journey touching Zone A and B charges 3.00
    assert fare_card.charge("Aldgate", "Balham", "2023-10-01") == 3.00

def test_multiple_journeys_within_zone_a():
    # Four Zone A journeys in one day: 2.50 + 2.50 + 2.00 + 0.00 = 7.00 (capped)
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    assert fare_card.charge("Aldgate", "Angel", "2023-10-01") == 0.00  # Capped at 7.00

def test_multiple_journeys_within_zone_b():
    # Four Zone B journeys in one day: 3.00 + 3.00 + 2.00 + 0.00 = 8.00 (capped)
    fare_card.charge("Balham", "Barbican", "2023-10-01")
    fare_card.charge("Balham", "Barbican", "2023-10-01")
    fare_card.charge("Balham", "Barbican", "2023-10-01")
    assert fare_card.charge("Balham", "Barbican", "2023-10-01") == 0.00  # Capped at 8.00

def test_daily_cap_with_zone_b_journey():
    # Zone A capped at 7.00; adding a Zone B journey raises cap to 8.00
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    fare_card.charge("Aldgate", "Angel", "2023-10-01")  # 2.50 + 2.50 + 2.00
    assert fare_card.charge("Balham", "Barbican", "2023-10-01") == 1.00  # Only charge 1.00

def test_journey_with_unknown_station():
    # Journey involving an unknown station should raise an error
    with pytest.raises(Exception):
        fare_card.charge("Aldgate", "UnknownStation", "2023-10-01")

def test_rejected_journey_does_not_charge():
    # A rejected journey charges nothing
    with pytest.raises(Exception):
        fare_card.charge("Aldgate", "UnknownStation", "2023-10-01")
    # The total remains unchanged after rejection
    assert fare_card.get_total() == 0.00

def test_weekly_cap_zone_a():
    # Three Zone A journeys every day for 6 days reach daily cap 40.00 for week
    for day in range(6):
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # Days 2 to 7
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day + 2:02d}")
    assert fare_card.get_total() == 40.00  # Total capped at 40.00

def test_monthly_cap_zone_a():
    # Three Zone A journeys every day of a month accumulate to 145.00
    for day in range(1, 31):  # Assuming 30 days in month
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")  # Daily charges
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")
    assert fare_card.get_total() == 145.00  # Total capped at 145.00

def test_daily_reset():
    # Ensure that a journey on the next calendar day charges the normal fare
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    fare_card.charge("Aldgate", "Angel", "2023-10-01")
    fare_card.charge("Aldgate", "Angel", "2023-10-01")  # Capped at 7.00
    assert fare_card.charge("Aldgate", "Angel", "2023-10-02") == 2.50  # New day, full fare

def test_weekly_reset():
    # Ensure that a journey on the following Monday charges normally after the prior ISO week reached its cap
    for day in range(1, 8):  # First week of October
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")  # 6 days
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")
    assert fare_card.charge("Aldgate", "Angel", "2023-10-09") == 2.50  # New week, full fare

def test_monthly_reset():
    # Ensure that a journey on the next calendar month charges normally after prior month reached its cap
    for day in range(1, 31):  # First month
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")  # 30 days
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")
        fare_card.charge("Aldgate", "Angel", f"2023-10-{day:02d}")
    assert fare_card.charge("Aldgate", "Angel", "2023-11-01") == 2.50  # New month, full fare

def test_unknown_origin_station():
    # Journey involving an unknown origin station should raise an error
    with pytest.raises(Exception):
        fare_card.charge("UnknownStation", "Aldgate", "2023-10-01")

def test_unknown_destination_station():
    # Journey involving an unknown destination station should raise an error
    with pytest.raises(Exception):
        fare_card.charge("Aldgate", "UnknownStation", "2023-10-01")

def test_running_total():
    # Test running total across valid journeys
    fare_card.charge("Aldgate", "Angel", "2023-10-01")  # 2.50
    fare_card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    fare_card.charge("Aldgate", "Balham", "2023-10-01")  # 3.00
    assert fare_card.get_total() == 8.50  # Total charged

def test_zone_b_weekly_cap():
    # Ensure Zone B weekly cap of 47.00
    for day in range(2, 9):  # First week of October
        fare_card.charge("Balham", "Barbican", f"2023-10-{day:02d}")  # 7 days
        fare_card.charge("Balham", "Barbican", f"2023-10-{day:02d}")
    assert fare_card.get_total() == 47.00  # Total capped at 47.00

def test_zone_b_monthly_cap():
    # Ensure Zone B monthly cap of 165.00
    for day in range(1, 31):  # 30 days in October
        fare_card.charge("Balham", "Barbican", f"2023-10-{day:02d}")  # Daily charges
        fare_card.charge("Balham", "Barbican", f"2023-10-{day:02d}")
        fare_card.charge("Balham", "Barbican", f"2023-10-{day:02d}")
    assert fare_card.get_total() == 165.00  # Total capped at 165.00

def test_parametrized_station_coverage():
    # Test valid journeys for all specified stations
    stations_a = ["Aldgate", "Amersham", "Anerley", "Angel", "Asterisk"]
    stations_b = ["Balham", "Barbican", "Bison", "Bugel", "Bullhead"]
    
    for station in stations_a:
        assert fare_card.charge(station, "Angel", "2023-10-01") == 2.50  # Zone A fare
        assert fare_card.charge("Angel", station, "2023-10-01") == 2.50  # Zone A fare

    for station in stations_b:
        assert fare_card.charge(station, "Barbican", "2023-10-01") == 3.00  # Zone B fare
        assert fare_card.charge("Barbican", station, "2023-10-01") == 3.00  # Zone B fare