import pytest
from solution import WeatherStation

def test_record_validated_readings():
    # Test AC-1.1: Humidity must be between 0 and 100
    station = WeatherStation()
    station.record_reading(1609459200, 25.0, 50.0, 1013.0)  # Valid reading
    # Valid boundary values
    station.record_reading(1609459260, 25.0, 0.0, 1013.0)   # Humidity = 0
    station.record_reading(1609459320, 25.0, 100.0, 1013.0) # Humidity = 100
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1609459380, 25.0, -1.0, 1013.0)
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1609459440, 25.0, 101.0, 1013.0)

    # Test AC-1.2: Pressure must be positive
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1609459500, 25.0, 50.0, 0.0)
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1609459560, 25.0, 50.0, -1.0)

    # Test AC-1.3: Current reading
    station.record_reading(1609459620, 26.0, 50.0, 1013.0)  # New valid reading
    assert station.current_reading() == (1609459620, 26.0, 50.0, 1013.0)  # The latest reading

    # Test AC-1.4: No current reading before any recordings
    new_station = WeatherStation()
    assert new_station.current_reading() is None

def test_temperature_statistics():
    station = WeatherStation()
    # Test AC-2.1: Minimum, maximum, and average temperature for all readings
    station.record_reading(1609459200, 20.0, 50.0, 1013.0)
    station.record_reading(1609459260, 25.0, 50.0, 1013.0)
    station.record_reading(1609459320, 30.0, 50.0, 1013.0)

    min_temp, max_temp, avg_temp = station.get_temperature_statistics()
    assert min_temp == 20.0  # Minimum temperature
    assert max_temp == 30.0  # Maximum temperature
    assert avg_temp == 25.0  # Average temperature: (20 + 25 + 30) / 3

    # Test AC-2.2: Start-only window statistics
    min_temp, max_temp, avg_temp = station.get_temperature_statistics(start_timestamp=1609459260)
    assert min_temp == 25.0  # Minimum in the window
    assert max_temp == 30.0  # Maximum in the window
    assert avg_temp == 27.5  # Average in the window: (25 + 30) / 2

    # Test AC-2.4: No readings in the window
    new_station = WeatherStation()
    with pytest.raises(Exception, match="no readings recorded"):
        new_station.get_temperature_statistics()

def test_windowed_temperature_statistics():
    station = WeatherStation()
    # Record readings
    station.record_reading(1609459200, 20.0, 50.0, 1013.0)
    station.record_reading(1609459260, 25.0, 50.0, 1013.0)
    station.record_reading(1609459320, 30.0, 50.0, 1013.0)

    # Test AC-2.2: Bound statistics by a start and end timestamp
    min_temp, max_temp, avg_temp = station.get_temperature_statistics(start_timestamp=1609459200, end_timestamp=1609459260)
    assert min_temp == 20.0  # Minimum in the window
    assert max_temp == 25.0  # Maximum in the window
    assert avg_temp == 22.5  # Average in the window: (20 + 25) / 2

    # Test AC-2.3: Readings outside the window are excluded
    min_temp, max_temp, avg_temp = station.get_temperature_statistics(start_timestamp=1609459260, end_timestamp=1609459320)
    assert min_temp == 25.0  # Minimum in the window
    assert max_temp == 30.0  # Maximum in the window
    assert avg_temp == 27.5  # Average in the window: (25 + 30) / 2

def test_temperature_trend():
    station = WeatherStation()
    # Test AC-3.1: Trend with zero or one reading is "steady"
    assert station.get_temperature_trend() == "steady"

    # Record readings
    station.record_reading(1609459200, 20.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"  # Only one reading

    station.record_reading(1609459260, 25.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"  # Two readings, increasing

    station.record_reading(1609459320, 30.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"  # Still rising

    station.record_reading(1609459380, 25.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"  # Zig-zag

    # Test AC-3.2: Two readings decreasing
    station.record_reading(1609459440, 20.0, 50.0, 1013.0)  # Decreasing
    assert station.get_temperature_trend() == "falling"  # Two readings, decreasing

    # Test AC-3.4: Trend with repeated temperatures
    station.record_reading(1609459500, 20.0, 50.0, 1013.0)  # Same as previous
    assert station.get_temperature_trend() == "steady"  # Repeated values

    # Test AC-3.4: Zig-zag trend, ending above
    station.record_reading(1609459560, 25.0, 50.0, 1013.0)  # Zig-zag
    station.record_reading(1609459620, 22.0, 50.0, 1013.0)  # Zig-zag
    assert station.get_temperature_trend() == "steady"  # Zig-zag

def test_display_notifications():
    station = WeatherStation()

    # Test AC-4.3 and AC-4.4: Display shows "No data" before any readings
    assert station.current_conditions_display() == "No data"
    assert station.statistics_display() == "No data"

    # Attach devices and record readings
    station.attach_display("current_conditions")
    station.attach_display("statistics")
    station.record_reading(1609459200, 25.0, 50.0, 1013.0)

    # Test current conditions display
    assert station.current_conditions_display() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"

    # Test statistics display
    min_temp, max_temp, avg_temp = station.get_temperature_statistics()
    assert station.statistics_display() == f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

    # Test multiple readings and their notifications
    station.record_reading(1609459260, 30.0, 50.0, 1013.0)
    assert station.current_conditions_display() == "Current conditions: 30.0°C, 50.0% humidity, 1013.0 hPa"
    min_temp, max_temp, avg_temp = station.get_temperature_statistics()
    assert station.statistics_display() == f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

def test_detach_display_notifications():
    station = WeatherStation()
    station.attach_display("current_conditions")
    station.attach_display("statistics")

    # Record first reading
    station.record_reading(1609459200, 25.0, 50.0, 1013.0)
    
    # Detach a display and check notifications
    station.detach_display("current_conditions")
    station.record_reading(1609459260, 30.0, 50.0, 1013.0)

    # Detached display should not receive updates
    assert station.current_conditions_display() == "Current conditions: 30.0°C, 50.0% humidity, 1013.0 hPa"  # Should retain last valid reading
    assert station.statistics_display() == "Temperature min 25.0°C, max 30.0°C, avg 27.5°C"  # Should show the statistics

    # Detach a never-attached display (silent ignore)
    station.detach_display("not_attached_display")

def test_temperature_alerts():
    station = WeatherStation()
    # Set thresholds
    station.set_temperature_thresholds(low=15.0, high=30.0)

    # Test AC-5.1: Above high threshold
    station.record_reading(1609459200, 35.0, 50.0, 1013.0)  # Should raise alert
    assert "ALERT: temperature 35.0°C above threshold 30.0°C" in station.get_alerts()  # Verify alert recorded

    # Test AC-5.2: Below low threshold
    station.record_reading(1609459260, 10.0, 50.0, 1013.0)  # Should raise alert
    assert "ALERT: temperature 10.0°C below threshold 15.0°C" in station.get_alerts()  # Verify alert recorded

    # Test AC-5.3: At threshold
    station.record_reading(1609459320, 15.0, 50.0, 1013.0)  # No alert
    station.record_reading(1609459380, 30.0, 50.0, 1013.0)  # No alert
    alerts_before = station.get_alerts()
    station.record_reading(1609459440, 15.0, 50.0, 1013.0)  # No alert
    station.record_reading(1609459500, 30.0, 50.0, 1013.0)  # No alert
    assert station.get_alerts() == alerts_before  # Verify no alert recorded