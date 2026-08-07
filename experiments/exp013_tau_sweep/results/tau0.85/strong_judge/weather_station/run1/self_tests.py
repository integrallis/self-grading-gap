import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()
    
    # AC-1.4: No current reading before anything has been recorded
    assert station.get_current_reading() is None
    
    # AC-1.1: Valid reading should be recorded
    station.record_reading("2023-10-01T12:00:00", 25.0, 50.0, 1013.0)  # Valid data
    assert station.get_current_reading() == ("2023-10-01T12:00:00", 25.0, 50.0, 1013.0)  # Current reading matches the input
    
    # AC-1.1: Humidity at lower boundary
    station.record_reading("2023-10-01T12:01:00", 22.0, 0.0, 1013.0)  # Valid data
    assert station.get_current_reading() == ("2023-10-01T12:01:00", 22.0, 0.0, 1013.0)  # Current reading matches the input

    # AC-1.1: Humidity at upper boundary
    station.record_reading("2023-10-01T12:02:00", 22.0, 100.0, 1013.0)  # Valid data
    assert station.get_current_reading() == ("2023-10-01T12:02:00", 22.0, 100.0, 1013.0)  # Current reading matches the input
    
    # AC-1.2: Invalid humidity (too low)
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading("2023-10-01T12:03:00", 22.0, -1.0, 1013.0)

    # AC-1.2: Invalid humidity (too high)
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading("2023-10-01T12:04:00", 22.0, 101.0, 1013.0)

    # AC-1.2: Invalid pressure (zero)
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading("2023-10-01T12:05:00", 22.0, 50.0, 0.0)

    # AC-1.2: Invalid pressure (negative)
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading("2023-10-01T12:06:00", 22.0, 50.0, -10.0)

    # AC-1.3: Record another valid reading
    station.record_reading("2023-10-01T12:07:00", 23.0, 55.0, 1012.0)
    assert station.get_current_reading() == ("2023-10-01T12:07:00", 23.0, 55.0, 1012.0)  # Check that the latest reading is current

    # AC-1.1: Ensure all readings are kept in arrival order
    readings = station.get_all_readings()  # Assume this method exists for testing
    assert readings == [
        ("2023-10-01T12:00:00", 25.0, 50.0, 1013.0),
        ("2023-10-01T12:01:00", 22.0, 0.0, 1013.0),
        ("2023-10-01T12:02:00", 22.0, 100.0, 1013.0),
        ("2023-10-01T12:07:00", 23.0, 55.0, 1012.0)
    ]


def test_temperature_statistics():
    station = WeatherStation()
    
    # AC-2.4: Asking for statistics when no readings recorded
    with pytest.raises(ValueError, match="no readings recorded"):
        station.get_temperature_statistics()

    # Record valid readings
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:01:00", 22.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:02:00", 18.0, 50.0, 1013.0)
    
    # AC-2.1: Get statistics covering all recorded readings
    min_temp, max_temp, avg_temp = station.get_temperature_statistics()  # should be (18.0, 22.0, (20.0 + 22.0 + 18.0) / 3)
    assert min_temp == 18.0
    assert max_temp == 22.0
    assert avg_temp == (20.0 + 22.0 + 18.0) / 3  # Average calculation
    
    # AC-2.2: Get statistics with a time window
    min_temp, max_temp, avg_temp = station.get_temperature_statistics("2023-10-01T12:00:00", "2023-10-01T12:01:00")
    assert min_temp == 20.0
    assert max_temp == 22.0
    assert avg_temp == (20.0 + 22.0) / 2  # Average calculation of the two readings
    
    # AC-2.2: Get statistics with a start-only time window
    min_temp, max_temp, avg_temp = station.get_temperature_statistics("2023-10-01T12:01:00")
    assert min_temp == 18.0  # Corrected from previous implementation
    assert max_temp == 22.0
    assert avg_temp == (22.0 + 18.0) / 2  # Average of the two readings
    
    # AC-2.2: Get statistics with an end-only time window
    min_temp, max_temp, avg_temp = station.get_temperature_statistics(end="2023-10-01T12:01:00")
    assert min_temp == 20.0
    assert max_temp == 22.0
    assert avg_temp == (20.0 + 22.0) / 2  # Average calculation of the two readings
    
    # AC-2.3: Readings outside the window should not be included
    min_temp, max_temp, avg_temp = station.get_temperature_statistics("2023-10-01T12:01:00", "2023-10-01T12:02:00")
    assert min_temp == 18.0
    assert max_temp == 22.0
    assert avg_temp == (22.0 + 18.0) / 2  # Average calculation of the two readings

    # AC-2.4: Asking for statistics when no readings qualify
    with pytest.raises(ValueError, match="no readings recorded"):
        station.get_temperature_statistics("2023-10-01T12:03:00", "2023-10-01T12:04:00")


def test_short_term_temperature_trend():
    station = WeatherStation()

    # AC-3.5: Zero readings should return steady
    assert station.get_temperature_trend() == "steady"

    # Record readings
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:01:00", 22.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:02:00", 21.0, 50.0, 1013.0)

    # AC-3.4: Should be steady (zig-zag)
    assert station.get_temperature_trend() == "steady"

    # AC-3.2: Should be rising with a new reading
    station.record_reading("2023-10-01T12:03:00", 23.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"

    # Record a new reading that decreases the trend
    station.record_reading("2023-10-01T12:04:00", 19.0, 50.0, 1013.0)

    # AC-3.4: Should be steady now
    assert station.get_temperature_trend() == "steady"

    # AC-3.2: Two readings rising
    station.record_reading("2023-10-01T12:05:00", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:06:00", 21.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"

    # AC-3.3: Two readings falling
    station.record_reading("2023-10-01T12:07:00", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:08:00", 19.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "falling"

    # AC-3.4: Zig-zag trend that ends above
    station.record_reading("2023-10-01T12:09:00", 20.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"

    # AC-3.4: Zig-zag trend that ends below
    station.record_reading("2023-10-01T12:10:00", 18.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"

    # AC-3.5: Test with exactly one reading
    station.record_reading("2023-10-01T12:11:00", 20.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"

    # AC-3.5: Test with exactly two readings rising
    station.record_reading("2023-10-01T12:12:00", 21.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"

    # AC-3.5: Test with exactly two readings falling
    station.record_reading("2023-10-01T12:13:00", 19.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "falling"


def test_notify_displays():
    station = WeatherStation()
    
    # AC-4.3: No data before any readings
    assert station.get_current_conditions_display() == "No data"

    # Attach the display
    station.attach_current_conditions_display()

    # Record a reading
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    
    # AC-4.1: Display should reflect the current conditions
    assert station.get_current_conditions_display() == "Current conditions: 20.0°C, 50.0% humidity, 1013.0 hPa"

    # Record another reading
    station.record_reading("2023-10-01T12:01:00", 22.0, 55.0, 1012.0)
    
    # AC-4.1: Display should reflect the new current conditions
    assert station.get_current_conditions_display() == "Current conditions: 22.0°C, 55.0% humidity, 1012.0 hPa"

    # Detach the display
    station.detach_current_conditions_display()
    
    # AC-4.2: Detached device should receive no further notifications
    station.record_reading("2023-10-01T12:02:00", 21.0, 60.0, 1011.0)
    assert station.get_current_conditions_display() == "Current conditions: 22.0°C, 55.0% humidity, 1012.0 hPa"  # No change

    # AC-4.2: Detaching a never-attached device is silently ignored
    station.detach_current_conditions_display()

    # AC-4.4: Test statistics display initial state
    assert station.get_statistics_display() == "No data"

    # Record readings for statistics display
    station.record_reading("2023-10-01T12:03:00", 21.0, 60.0, 1011.0)
    station.record_reading("2023-10-01T12:04:00", 22.0, 55.0, 1012.0)

    # AC-4.4: Ensure statistics display shows updated values
    assert station.get_statistics_display() == "Temperature min 21.0°C, max 22.0°C, avg 21.0°C"


def test_temperature_alerts():
    station = WeatherStation()
    
    # Setting thresholds
    station.set_temperature_thresholds(15.0, 25.0)
    
    # AC-5.3: Reading at the threshold should not raise an alert
    station.record_reading("2023-10-01T12:00:00", 25.0, 50.0, 1013.0)
    assert station.get_alerts() == []  # No alerts

    # AC-5.1: Reading above the threshold should raise an alert
    station.record_reading("2023-10-01T12:01:00", 26.0, 50.0, 1013.0)
    assert station.get_alerts() == ["ALERT: temperature 26.0°C above threshold 25.0°C"]

    # AC-5.2: Reading below the threshold should raise an alert
    station.record_reading("2023-10-01T12:02:00", 14.0, 50.0, 1013.0)
    assert station.get_alerts() == [
        "ALERT: temperature 26.0°C above threshold 25.0°C",
        "ALERT: temperature 14.0°C below threshold 15.0°C"
    ]

    # AC-5.3: Reading exactly at the low threshold should not raise an alert
    station.record_reading("2023-10-01T12:03:00", 15.0, 50.0, 1013.0)
    assert station.get_alerts() == [
        "ALERT: temperature 26.0°C above threshold 25.0°C",
        "ALERT: temperature 14.0°C below threshold 15.0°C"
    ]