# test_weather_station.py

from solution import WeatherStation
import pytest

def test_record_validated_readings():
    station = WeatherStation()

    # Test AC-1.4: Before anything has been recorded there is no current reading.
    assert station.current_reading() is None

    # Test AC-1.1: Valid reading
    station.record_reading(timestamp=1, temperature=20.0, humidity=50.0, pressure=1013.0)
    assert station.current_reading() == (1, 20.0, 50.0, 1013.0)  # Latest reading should match

    # Test AC-1.1: Invalid humidity (too low)
    with pytest.raises(ValueError) as e:
        station.record_reading(timestamp=2, temperature=21.0, humidity=-1.0, pressure=1013.0)
    assert "humidity must be between 0 and 100" in str(e.value)

    # Test AC-1.1: Invalid humidity (too high)
    with pytest.raises(ValueError) as e:
        station.record_reading(timestamp=3, temperature=22.0, humidity=101.0, pressure=1013.0)
    assert "humidity must be between 0 and 100" in str(e.value)

    # Test AC-1.1: Valid humidity boundary (exactly 0)
    station.record_reading(timestamp=4, temperature=23.0, humidity=0.0, pressure=1013.0)
    assert station.current_reading() == (4, 23.0, 0.0, 1013.0)

    # Test AC-1.1: Valid humidity boundary (exactly 100)
    station.record_reading(timestamp=5, temperature=24.0, humidity=100.0, pressure=1013.0)
    assert station.current_reading() == (5, 24.0, 100.0, 1013.0)

    # Test AC-1.2: Invalid pressure (zero)
    with pytest.raises(ValueError) as e:
        station.record_reading(timestamp=6, temperature=25.0, humidity=55.0, pressure=0.0)
    assert "pressure must be positive" in str(e.value)

    # Test AC-1.2: Invalid pressure (negative)
    with pytest.raises(ValueError) as e:
        station.record_reading(timestamp=7, temperature=26.0, humidity=55.0, pressure=-1.0)
    assert "pressure must be positive" in str(e.value)

    # Test AC-1.3: Keep readings in order and report the latest
    station.record_reading(timestamp=8, temperature=27.0, humidity=55.0, pressure=1013.0)
    assert station.current_reading() == (8, 27.0, 55.0, 1013.0)  # Latest reading should match

def test_temperature_statistics():
    station = WeatherStation()

    # Test AC-2.4: No readings recorded
    with pytest.raises(ValueError) as e:
        station.temperature_statistics()
    assert "no readings recorded" in str(e.value)

    # Record some readings
    station.record_reading(timestamp=1, temperature=20.0, humidity=50.0, pressure=1013.0)
    station.record_reading(timestamp=2, temperature=25.0, humidity=50.0, pressure=1013.0)
    station.record_reading(timestamp=3, temperature=15.0, humidity=50.0, pressure=1013.0)

    # Test AC-2.1: Statistics over all readings
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 15.0  # min is 15.0
    assert max_temp == 25.0  # max is 25.0
    assert avg_temp == 20.0  # avg is (20 + 25 + 15) / 3 = 20.0

    # Test AC-2.2: Start-only window statistics
    min_temp, max_temp, avg_temp = station.temperature_statistics(start_timestamp=1)
    assert min_temp == 15.0  # min is 15.0
    assert max_temp == 25.0  # max is 25.0
    assert avg_temp == 20.0  # avg is 20.0

    # Test AC-2.2: End-only window statistics
    min_temp, max_temp, avg_temp = station.temperature_statistics(end_timestamp=2)
    assert min_temp == 20.0  # min is 20.0
    assert max_temp == 25.0  # max is 25.0
    assert avg_temp == 22.5  # avg is (20 + 25) / 2 = 22.5

    # Test AC-2.2: Full window statistics
    min_temp, max_temp, avg_temp = station.temperature_statistics(start_timestamp=1, end_timestamp=2)
    assert min_temp == 20.0  # min is 20.0
    assert max_temp == 25.0  # max is 25.0
    assert avg_temp == 22.5  # avg is (20 + 25) / 2 = 22.5

    # Test AC-2.3: No readings in window
    with pytest.raises(ValueError) as e:
        station.temperature_statistics(start_timestamp=4, end_timestamp=5)
    assert "no readings recorded" in str(e.value)

def test_temperature_trend():
    station = WeatherStation()

    # Test AC-3.5: Zero readings
    assert station.temperature_trend() == "steady"

    # Add readings
    station.record_reading(timestamp=1, temperature=20.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "steady"  # Only one reading

    station.record_reading(timestamp=2, temperature=21.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "rising"  # Two readings, rising

    station.record_reading(timestamp=3, temperature=22.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "rising"  # Three readings, still rising

    station.record_reading(timestamp=4, temperature=21.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "steady"  # Three readings, zig-zag

    station.record_reading(timestamp=5, temperature=21.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "steady"  # Three readings, steady

    # Test AC-3.2: Two readings, strictly decreasing
    station.record_reading(timestamp=6, temperature=22.0, humidity=50.0, pressure=1013.0)
    station.record_reading(timestamp=7, temperature=21.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "falling"  # Two readings, falling

    # Test AC-3.1: Only the three most recent readings are considered
    station.record_reading(timestamp=8, temperature=20.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "falling"  # Three most recent are [22.0, 21.0, 20.0]

    # Test AC-3.4: A zig-zag trend case ending above where it started
    station.record_reading(timestamp=9, temperature=22.0, humidity=50.0, pressure=1013.0)
    assert station.temperature_trend() == "steady"  # Three most recent are [20.0, 22.0, 21.0]

def test_notify_attached_displays():
    station = WeatherStation()
    station.attach_display("display1")
    station.attach_display("display2")
    
    # Test AC-4.3: Initial state of displays
    assert station.current_conditions_display() == "No data"
    assert station.statistics_display() == "No data"

    # Record a reading
    station.record_reading(timestamp=1, temperature=20.0, humidity=50.0, pressure=1013.0)
    
    # Test AC-4.3: Current conditions display updates
    assert station.current_conditions_display() == "Current conditions: 20.0°C, 50.0% humidity, 1013.0 hPa"
    
    # Test AC-4.4: Statistics display updates
    assert station.statistics_display() == "Temperature min 20.0°C, max 20.0°C, avg 20.0°C"

    # Verify that all displays are notified (the details of notifications are not specified)
    # Test AC-4.1: Verify that all displays are notified
    station.record_reading(timestamp=2, temperature=21.0, humidity=60.0, pressure=1013.0)
    assert station.current_conditions_display() == "Current conditions: 21.0°C, 60.0% humidity, 1013.0 hPa"
    assert station.statistics_display() == "Temperature min 20.0°C, max 21.0°C, avg 20.5°C"

    # Detach a display and verify it no longer receives updates
    station.detach_display("display1")
    station.record_reading(timestamp=3, temperature=22.0, humidity=65.0, pressure=1013.0)
    assert station.current_conditions_display() == "Current conditions: 22.0°C, 65.0% humidity, 1013.0 hPa"
    assert station.statistics_display() == "Temperature min 20.0°C, max 22.0°C, avg 21.0°C"

    # Verify that the detached display did not receive the latest update
    station.detach_display("display3")  # Detaching a non-attached display should not raise an error
    assert station.current_conditions_display() == "Current conditions: 22.0°C, 65.0% humidity, 1013.0 hPa"

def test_temperature_alerts():
    station = WeatherStation()
    station.set_thresholds(low=15.0, high=25.0)

    # Test AC-5.3: No alert at threshold
    station.record_reading(timestamp=1, temperature=15.0, humidity=50.0, pressure=1013.0)
    assert station.alerts() == []

    station.record_reading(timestamp=2, temperature=25.0, humidity=50.0, pressure=1013.0)
    assert station.alerts() == []

    # Test AC-5.1: Alert above threshold
    station.record_reading(timestamp=3, temperature=26.0, humidity=50.0, pressure=1013.0)
    assert station.alerts() == ["ALERT: temperature 26.0°C above threshold 25.0°C"]

    # Test AC-5.2: Alert below threshold
    station.record_reading(timestamp=4, temperature=14.0, humidity=50.0, pressure=1013.0)
    assert station.alerts() == [
        "ALERT: temperature 26.0°C above threshold 25.0°C",
        "ALERT: temperature 14.0°C below threshold 15.0°C"
    ]