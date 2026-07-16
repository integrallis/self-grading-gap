import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()

    # AC-1.1: Valid reading
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    assert station.current_reading is not None  # Current reading should be the latest valid reading

    # AC-1.1: Invalid humidity above 100, should raise error
    with pytest.raises(Exception) as exc:
        station.record_reading("2023-10-01T12:00:00", 20.0, 150.0, 1013.0)
    assert str(exc.value) == "humidity must be between 0 and 100"

    # AC-1.1: Invalid humidity below 0, should raise error
    with pytest.raises(Exception) as exc:
        station.record_reading("2023-10-01T12:00:00", 20.0, -1.0, 1013.0)
    assert str(exc.value) == "humidity must be between 0 and 100"

    # AC-1.2: Invalid pressure of zero, should raise error
    with pytest.raises(Exception) as exc:
        station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 0.0)
    assert str(exc.value) == "pressure must be positive"

    # AC-1.2: Invalid pressure, should raise error
    with pytest.raises(Exception) as exc:
        station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, -1.0)
    assert str(exc.value) == "pressure must be positive"

    # AC-1.3: Keeping readings in order
    station.record_reading("2023-10-01T12:01:00", 21.0, 55.0, 1014.0)
    assert station.current_reading is not None  # Current reading should now be latest valid reading
    assert station.current_reading.temperature == 21.0  # Current reading should be last recorded reading

    # AC-1.4: No current reading before any records
    empty_station = WeatherStation()
    assert empty_station.current_reading is None


def test_temperature_statistics_over_time_window():
    station = WeatherStation()
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:01:00", 21.0, 55.0, 1014.0)
    station.record_reading("2023-10-01T12:02:00", 22.0, 60.0, 1013.5)

    # AC-2.1: Statistics over all readings
    min_temp, max_temp, avg_temp = station.get_temperature_statistics()
    assert min_temp == 20.0  # min of [20.0, 21.0, 22.0]
    assert max_temp == 22.0  # max of [20.0, 21.0, 22.0]
    assert avg_temp == 21.0  # avg of [20.0, 21.0, 22.0] is (20 + 21 + 22) / 3

    # AC-2.2: Start-only windowed statistics
    min_temp, max_temp, avg_temp = station.get_temperature_statistics("2023-10-01T12:01:00")
    assert min_temp == 21.0  # min of [21.0, 22.0]
    assert max_temp == 22.0  # max of [21.0, 22.0]
    assert avg_temp == 21.5  # avg of [21.0, 22.0] is (21 + 22) / 2

    # AC-2.3: End-only windowed statistics
    min_temp, max_temp, avg_temp = station.get_temperature_statistics(end="2023-10-01T12:02:00")
    assert min_temp == 20.0  # min of [20.0, 21.0]
    assert max_temp == 21.0  # max of [20.0, 21.0]
    assert avg_temp == 20.5  # avg of [20.0, 21.0] is (20 + 21) / 2

    # AC-2.3: Exclusion after the end bound
    station.record_reading("2023-10-01T12:03:00", 23.0, 65.0, 1015.0)
    min_temp, max_temp, avg_temp = station.get_temperature_statistics("2023-10-01T12:01:00", "2023-10-01T12:02:00")
    assert min_temp == 21.0  # min of [21.0, 22.0]
    assert max_temp == 22.0  # max of [21.0, 22.0]
    assert avg_temp == 21.5  # avg of [21.0, 22.0] is (21 + 22) / 2

    # AC-2.4: No readings recorded
    empty_station = WeatherStation()
    with pytest.raises(Exception) as exc:
        empty_station.get_temperature_statistics()
    assert str(exc.value) == "no readings recorded"

    # AC-2.4: No readings in window
    with pytest.raises(Exception) as exc:
        station.get_temperature_statistics("2023-10-01T12:04:00", "2023-10-01T12:05:00")
    assert str(exc.value) == "no readings recorded"


def test_short_term_temperature_trend():
    station = WeatherStation()
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:01:00", 21.0, 55.0, 1014.0)
    station.record_reading("2023-10-01T12:02:00", 22.0, 60.0, 1013.5)

    # AC-3.2: Trend is rising
    assert station.get_temperature_trend() == "rising"

    # Add a reading that causes a falling trend
    station.record_reading("2023-10-01T12:03:00", 21.0, 55.0, 1014.0)
    assert station.get_temperature_trend() == "falling"  # Two readings decreasing

    # Add a reading that is steady
    station.record_reading("2023-10-01T12:04:00", 21.0, 55.0, 1014.0)
    assert station.get_temperature_trend() == "steady"  # Zig-zag trend

    # AC-3.5: Zero or one reading
    single_reading_station = WeatherStation()
    single_reading_station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    assert single_reading_station.get_temperature_trend() == "steady"

    # AC-3.5: Zero readings
    empty_trend_station = WeatherStation()
    assert empty_trend_station.get_temperature_trend() == "steady"

    # Test for a zig-zag ending above the starting temperature
    station.record_reading("2023-10-01T12:05:00", 23.0, 65.0, 1015.0)
    station.record_reading("2023-10-01T12:06:00", 22.0, 65.0, 1015.0)
    assert station.get_temperature_trend() == "steady"  # Zig-zag trend

    # Test for a zig-zag ending below the starting temperature
    station.recording("2023-10-01T12:07:00", 20.0, 65.0, 1015.0)
    assert station.get_temperature_trend() == "steady"  # Zig-zag trend


def test_notify_attached_displays():
    class MockDisplay:
        def __init__(self):
            self.latest_reading = "No data"
            self.temperature_stats = "No data"

        def update_reading(self, temperature, humidity, pressure):
            self.latest_reading = f"Current conditions: {temperature}°C, {humidity}% humidity, {pressure} hPa"

        def update_statistics(self, min_temp, max_temp, avg_temp):
            self.temperature_stats = f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

    station = WeatherStation()
    display1 = MockDisplay()
    display2 = MockDisplay()

    station.attach_display(display1)
    station.attach_display(display2)
    station.record_reading("2023-10-01T12:00:00", 20.0, 50.0, 1013.0)
    assert display1.latest_reading == "Current conditions: 20.0°C, 50.0% humidity, 1013.0 hPa"
    assert display2.latest_reading == "Current conditions: 20.0°C, 50.0% humidity, 1013.0 hPa"

    # AC-4.2: Detach device
    station.detach_display(display1)
    station.record_reading("2023-10-01T12:01:00", 21.0, 55.0, 1014.0)
    assert display1.latest_reading == "Current conditions: 20.0°C, 50.0% humidity, 1013.0 hPa"  # No update for detached
    assert display2.latest_reading == "Current conditions: 21.0°C, 55.0% humidity, 1014.0 hPa"  # Update for attached

    # Test for detaching a device that was never attached
    mock_display3 = MockDisplay()
    station.detach_display(mock_display3)  # Should be silently ignored
    assert display2.latest_reading == "Current conditions: 21.0°C, 55.0% humidity, 1014.0 hPa"  # No change


def test_raise_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(low=15.0, high=25.0)

    # AC-5.1: Above threshold
    with pytest.raises(Exception) as exc:
        station.record_reading("2023-10-01T12:00:00", 26.0, 50.0, 1013.0)  # Should raise alert
    assert str(exc.value) == "ALERT: temperature 26.0°C above threshold 25.0°C"

    # AC-5.2: Below threshold
    with pytest.raises(Exception) as exc:
        station.record_reading("2023-10-01T12:01:00", 14.0, 50.0, 1013.0)  # Should raise alert
    assert str(exc.value) == "ALERT: temperature 14.0°C below threshold 15.0°C"

    # AC-5.3: At threshold, no alert
    station.record_reading("2023-10-01T12:02:00", 15.0, 50.0, 1013.0)  # No alert should be raised