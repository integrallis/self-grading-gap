import pytest
from solution import TransitCard

def test_zone_a_whole_journey_charge():
    card = TransitCard()
    charge = card.journey('Aldgate', 'Anerley', '2023-10-01')  # Zone A
    assert charge == 2.50  # AC-1.1

def test_zone_b_whole_journey_charge():
    card = TransitCard()
    charge = card.journey('Balham', 'Bison', '2023-10-01')  # Zone B
    assert charge == 3.00  # AC-1.2

def test_zone_a_and_b_journey_charge():
    card = TransitCard()
    charge = card.journey('Aldgate', 'Balham', '2023-10-01')  # Zone A to Zone B
    assert charge == 3.00  # AC-1.2

def test_journey_reports_charge():
    card = TransitCard()
    charge = card.journey('Aldgate', 'Anerley', '2023-10-01')
    assert charge == 2.50  # AC-1.4

def test_daily_cap_zone_a():
    card = TransitCard()
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    charge = card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    assert charge == 2.50  # AC-2.1
    charge = card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.00
    assert charge == 2.00  # AC-2.1
    charge = card.journey('Aldgate', 'Anerley', '2023-10-01')  # 0.00
    assert charge == 0.00  # AC-2.1

def test_daily_cap_zone_b():
    card = TransitCard()
    card.journey('Balham', 'Bison', '2023-10-01')  # 3.00
    charge = card.journey('Balham', 'Bison', '2023-10-01')  # 3.00
    assert charge == 3.00  # AC-2.2
    charge = card.journey('Balham', 'Bison', '2023-10-01')  # 2.00
    assert charge == 2.00  # AC-2.2
    charge = card.journey('Balham', 'Bison', '2023-10-01')  # 0.00
    assert charge == 0.00  # AC-2.2

def test_daily_cap_zone_b_affecting_zone_a():
    card = TransitCard()
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.00
    charge = card.journey('Balham', 'Bison', '2023-10-01')  # 1.00
    assert charge == 1.00  # AC-2.4

def test_weekly_cap_zone_a():
    card = TransitCard()
    for day in range(2, 8):  # Six days in one ISO week (2023-10-02 to 2023-10-07)
        for _ in range(3):  # Three Zone A journeys each day
            card.journey('Aldgate', 'Anerley', f'2023-10-{day:02}')  # 2.50 each
    # The total should be capped at 40.00 for the week
    total = card.get_total()  # Assume this method exists
    assert total == 40.00  # AC-3.1

def test_weekly_cap_zone_a_next_week():
    card = TransitCard()
    for day in range(2, 8):  # Six days in one ISO week
        for _ in range(3):  # Three Zone A journeys each day
            card.journey('Aldgate', 'Anerley', f'2023-10-{day:02}')  # 2.50 each
    charge = card.journey('Aldgate', 'Anerley', '2023-10-09')  # New ISO week
    assert charge == 2.50  # AC-3.2

def test_weekly_cap_zone_b():
    card = TransitCard()
    for day in range(2, 8):  # Six days in one ISO week
        for _ in range(3):  # Three Zone B journeys each day
            card.journey('Balham', 'Bison', f'2023-10-{day:02}')  # 3.00 each
    total = card.get_total()  # Assume this method exists
    assert total == 47.00  # AC-3.1

def test_monthly_cap_zone_a():
    card = TransitCard()
    for day in range(1, 32):  # Simulate 31 days
        for _ in range(3):  # Three journeys each day
            card.journey('Aldgate', 'Anerley', f'2023-10-{day:02}')  # 2.50 each
    total = card.get_total()  # Assume this method exists
    assert total == 145.00  # AC-3.3

def test_monthly_cap_zone_b():
    card = TransitCard()
    for day in range(1, 32):  # Simulate 31 days
        for _ in range(3):  # Three journeys each day
            card.journey('Balham', 'Bison', f'2023-10-{day:02}')  # 3.00 each
    total = card.get_total()  # Assume this method exists
    assert total == 165.00  # AC-3.3

def test_next_day_charge_after_cap():
    card = TransitCard()
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.00
    charge = card.journey('Aldgate', 'Anerley', '2023-10-02')  # Should charge full fare
    assert charge == 2.50  # AC-2.3

def test_unknown_station_journey():
    card = TransitCard()
    with pytest.raises(Exception) as exc_info:  # Expecting an error
        card.journey('Unknown', 'Anerley', '2023-10-01')
    assert 'Unknown' in str(exc_info.value)  # AC-4.1

def test_unknown_station_journey_total_unchanged():
    card = TransitCard()
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    with pytest.raises(Exception) as exc_info:  # Expecting an error
        card.journey('Unknown', 'Anerley', '2023-10-01')  # Unknown station
    assert 'Unknown' in str(exc_info.value)  # AC-4.1
    total = card.get_total()  # Assume this method exists
    assert total == 2.50  # AC-4.2, total should remain unchanged

def test_unknown_destination_station():
    card = TransitCard()
    with pytest.raises(Exception) as exc_info:  # Expecting an error
        card.journey('Aldgate', 'Unknown', '2023-10-01')
    assert 'Unknown' in str(exc_info.value)  # AC-4.1

def test_running_total():
    card = TransitCard()
    card.journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.journey('Balham', 'Bison', '2023-10-01')  # 3.00
    total = card.get_total()  # Assume this method exists
    assert total == 5.50  # AC-5.1

def test_zone_a_stations():
    stations = [
        ('Aldgate', 2.50),
        ('Amersham', 2.50),
        ('Anerley', 2.00),  # Should be 2.00 due to cap
        ('Angel', 0.00),    # Should be 0.00 due to cap
        ('Asterisk', 0.00)  # Should be 0.00 due to cap
    ]
    for station, fare in stations:
        card = TransitCard()
        charge = card.journey(station, 'Anerley', '2023-10-01')
        assert charge == fare  # Validate Zone A stations

def test_zone_b_stations():
    stations = [
        ('Balham', 3.00),
        ('Barbican', 3.00),
        ('Bison', 2.00),  # Should be 2.00 due to cap
        ('Bugel', 0.00),   # Should be 0.00 due to cap
        ('Bullhead', 0.00)  # Should be 0.00 due to cap
    ]
    for station, fare in stations:
        card = TransitCard()
        charge = card.journey(station, 'Bison', '2023-10-01')
        assert charge == fare  # Validate Zone B stations