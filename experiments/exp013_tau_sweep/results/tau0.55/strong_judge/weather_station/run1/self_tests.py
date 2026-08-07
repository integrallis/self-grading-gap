import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()
    
    # AC-1.4: Before anything has been recorded, there is no current reading.
    # No assertion needed; the specification only states there is no current reading.
    
    # AC-1.1: Valid reading
    station.record_reading(1622548800, 25.0, 50.0, 1013.0)  # timestamp, temp, humidity, pressure
    assert station.current_reading() == (1622548800, 25.0, 50.0, 1013.0)  # current reading should be the one recorded

    # AC-1.1: Invalid humidity (should raise error)
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading(1622548810, 25.0, 150.0, 1013.0)
    
    # AC-1.1: Valid humidity
    station.record_reading(1622548820, 25.0, 0.0, 1013.0)  # Test lower boundary
    station.record_reading(1622548830, 25.0, 100.0, 1013.0)  # Test upper boundary
    
    # AC-1.1: Invalid humidity (should raise error)
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading(1622548840, 25.0, -1.0, 1013.0)
    
    # AC-1.2: Invalid pressure (should raise error)
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading(1622548850, 25.0, 50.0, -1.0)
    
    # AC-1.2: Invalid pressure (should raise error)
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading(1622548860, 25.0, 50.0, 0.0)

    # AC-1.3: After multiple readings, the current reading should be the last recorded
    station.record_reading(1622548870, 26.0, 50.0, 1013.0)
    assert station.current_reading() == (1622548870, 26.0, 50.0, 1013.0)

def test_temperature_statistics():
    station = WeatherStation()
    
    # AC-2.4: Asking for statistics when no readings qualify
    with pytest.raises(ValueError, match="no readings recorded"):
        station.get_temperature_statistics()
    
    # Record valid readings
    station.record_reading(1622548800, 20.0, 50.0, 1013.0)
    station.record_reading(1622548810, 25.0, 50.0, 1013.0)
    station.record_reading(1622548820, 30.0, 50.0, 1013.0)
    
    # AC-2.1: Statistics over all readings
    stats = station.get_temperature_statistics()
    assert stats['min'] == 20.0  # min of (20.0, 25.0, 30.0)
    assert stats['max'] == 30.0  # max of (20.0, 25.0, 30.0)
    assert stats['avg'] == 25.0  # avg of (20.0 + 25.0 + 30.0) / 3
    
    # AC-2.2: Windowed statistics with both start and end bounds
    stats_window = station.get_temperature_statistics(start=1622548800, end=1622548810)
    assert stats_window['min'] == 20.0
    assert stats_window['max'] == 25.0
    assert stats_window['avg'] == 22.5  # avg of (20.0 + 25.0) / 2
    
    # AC-2.2: Windowed statistics, exact start inclusion
    stats_window_start_inclusive = station.get_temperature_statistics(start=1622548800)
    assert stats_window_start_inclusive['min'] == 20.0
    assert stats_window_start_inclusive['max'] == 30.0
    assert stats_window_start_inclusive['avg'] == 25.0  # avg of (20.0 + 25.0 + 30.0) / 3

    # AC-2.3: Readings outside the window are excluded
    stats_window_after = station.get_temperature_statistics(start=1622548815)
    assert stats_window_after['min'] == 30.0  # only one reading in this window
    assert stats_window_after['max'] == 30.0
    assert stats_window_after['avg'] == 30.0

    # AC-2.4: No qualifying readings in the window
    with pytest.raises(ValueError, match="no readings recorded"):
        station.get_temperature_statistics(start=1622548850, end=1622548860)

def test_temperature_trend():
    station = WeatherStation()
    
    # AC-3.5: With zero readings, the trend is steady
    assert station.get_temperature_trend() == "steady"
    
    # Record valid readings
    station.record_reading(1622548800, 20.0, 50.0, 1013.0)
    station.record_reading(1622548810, 25.0, 50.0, 1013.0)
    
    # AC-3.2: Strictly increasing temperatures
    assert station.get_temperature_trend() == "rising"
    
    # Add a same temperature reading
    station.record_reading(1622548820, 30.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"  # AC-3.4: repeated values
    
    # Add a decreasing reading
    station.record_reading(1622548830, 28.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "steady"  # AC-3.4: zig-zag
    
    # Add a further decreasing reading
    station.record_reading(1622548840, 25.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"  # AC-3.2: strictly increasing

    # AC-3.2: Two-reading rising trend
    station.record_reading(1622548850, 26.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "rising"  # AC-3.2: strictly increasing

    # AC-3.3: Two-reading falling trend
    station.record_reading(1622548860, 24.0, 50.0, 1013.0)
    assert station.get_temperature_trend() == "falling"  # AC-3.3: strictly decreasing
    
    # AC-3.5: One reading trend is steady
    station.record_reading(1622548870, 25.0, 50.0, 1013.0)  # back to steady
    assert station.get_temperature_trend() == "steady"  # AC-3.5: one reading

def test_notify_display_on_recording():
    station = WeatherStation()
    display1 = station.attach_display()
    display2 = station.attach_display()
    
    # AC-4.3: Display shows "No data" before it has received anything
    assert display1.render() == "No data"
    assert display2.render() == "No data"
    
    # Record a reading
    station.record_reading(1622548800, 25.0, 50.0, 1013.0)
    assert display1.render() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"  # AC-4.3
    assert display2.render() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"  # AC-4.3
    
    # Detach display1
    station.detach_display(display1)
    station.record_reading(1622548810, 30.0, 50.0, 1013.0)
    assert display1.render() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"  # AC-4.2: detached device receives nothing
    assert display2.render() == "Current conditions: 30.0°C, 50.0% humidity, 1013.0 hPa"  # AC-4.1: still attached
    
    # Test detaching a device that was never attached
    display3 = object()  # this is a pretend display that was never attached
    station.detach_display(display3)  # should silently ignore
    
    # Record another reading
    station.record_reading(1622548820, 28.0, 50.0, 1013.0)
    assert display1.render() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"  # still no update
    assert display2.render() == "Current conditions: 28.0°C, 50.0% humidity, 1013.0 hPa"  # Updated reading

def test_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(low=15.0, high=25.0)
    
    # AC-5.3: A reading exactly at a threshold raises no alert
    station.record_reading(1622548800, 25.0, 50.0, 1013.0)
    assert station.get_alerts() == []  # No alerts
    
    # AC-5.1: A reading strictly above the configured high threshold
    station.record_reading(1622548810, 30.0, 50.0, 1013.0)
    assert station.get_alerts() == ["ALERT: temperature 30.0°C above threshold 25.0°C"]
    
    # AC-5.2: A reading strictly below the configured low threshold
    station.record_reading(1622548820, 10.0, 50.0, 1013.0)
    assert station.get_alerts() == [
        "ALERT: temperature 30.0°C above threshold 25.0°C",
        "ALERT: temperature 10.0°C below threshold 15.0°C"
    ]

    # AC-5.3: Low threshold equality test
    station.record_reading(1622548830, 15.0, 50.0, 1013.0)  # exactly at low threshold
    assert station.get_alerts() == [
        "ALERT: temperature 30.0°C above threshold 25.0°C",
        "ALERT: temperature 10.0°C below threshold 15.0°C"
    ]