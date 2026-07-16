import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()
    
    # AC-1.1: Valid reading
    station.record_reading(1622547800, 25.0, 60.0, 1013.2)  # timestamp, temperature, humidity, pressure
    assert station.current_reading == (1622547800, 25.0, 60.0, 1013.2)  # current reading should be the recorded one

    # AC-1.1: Invalid humidity
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1622547801, 25.0, -1.0, 1013.2)
    
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1622547802, 25.0, 101.0, 1013.2)

    # AC-1.2: Invalid pressure
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1622547803, 25.0, 60.0, 0)
    
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1622547804, 25.0, 60.0, -1)

    # AC-1.3: Keep readings in order
    station.record_reading(1622547805, 26.0, 65.0, 1015.0)
    assert station.current_reading == (1622547805, 26.0, 65.0, 1015.0)  # current reading should be the latest one

    # AC-1.4: No current reading before any recording
    new_station = WeatherStation()
    assert new_station.current_reading is None  # no current reading before any recording

def test_temperature_statistics():
    station = WeatherStation()
    station.record_reading(1622547800, 25.0, 60.0, 1013.2)
    station.record_reading(1622547801, 30.0, 65.0, 1015.0)
    station.record_reading(1622547802, 20.0, 70.0, 1010.0)
    
    # AC-2.1: Overall statistics
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 20.0  # min of [25.0, 30.0, 20.0]
    assert max_temp == 30.0  # max of [25.0, 30.0, 20.0]
    assert avg_temp == 25.0  # average of [25.0, 30.0, 20.0] is (25 + 30 + 20) / 3 = 25.0

    # AC-2.2: Window statistics with start timestamp
    min_temp, max_temp, avg_temp = station.temperature_statistics(start=1622547801)
    assert min_temp == 30.0  # only consider [30.0, 20.0]
    assert max_temp == 30.0
    assert avg_temp == 25.0  # average of [30.0, 20.0] is (30 + 20) / 2 = 25.0

    # AC-2.2: Window statistics with end timestamp
    min_temp, max_temp, avg_temp = station.temperature_statistics(end=1622547801)
    assert min_temp == 25.0  # only consider [25.0, 30.0]
    assert max_temp == 30.0
    assert avg_temp == 27.5  # average of [25.0, 30.0] is (25 + 30) / 2 = 27.5

    # AC-2.2: Window statistics with both start and end timestamps
    min_temp, max_temp, avg_temp = station.temperature_statistics(start=1622547800, end=1622547802)
    assert min_temp == 20.0  # consider [25.0, 30.0, 20.0]
    assert max_temp == 30.0
    assert avg_temp == 25.0  # average of [25.0, 30.0, 20.0] is (25 + 30 + 20) / 3 = 25.0

    # AC-2.4: No readings recorded
    empty_station = WeatherStation()
    with pytest.raises(Exception, match="no readings recorded"):
        empty_station.temperature_statistics()

def test_temperature_trend():
    station = WeatherStation()
    
    # AC-3.5: No readings results in steady
    assert station.temperature_trend() == "steady"

    station.record_reading(1622547800, 20.0, 50.0, 1010.0)
    # AC-3.5: One reading results in steady
    assert station.temperature_trend() == "steady"

    station.record_reading(1622547801, 21.0, 55.0, 1011.0)
    # AC-3.2: Two readings, strictly increasing
    assert station.temperature_trend() == "rising"

    station.record_reading(1622547802, 22.0, 60.0, 1012.0)
    # AC-3.2: Three readings, strictly increasing
    assert station.temperature_trend() == "rising"

    station.record_reading(1622547803, 21.5, 65.0, 1013.0)
    # AC-3.4: Not strictly increasing (zig-zag)
    assert station.temperature_trend() == "steady"

    station.record_reading(1622547804, 20.0, 70.0, 1010.0)
    # AC-3.3: Strictly decreasing
    assert station.temperature_trend() == "falling"

    station.record_reading(1622547805, 19.0, 75.0, 1005.0)
    # AC-3.4: Not strictly increasing (zig-zag)
    assert station.temperature_trend() == "steady"

def test_notify_attached_displays():
    class MockDisplay:
        def __init__(self):
            self.last_update = "No data"

        def update(self, reading):
            self.last_update = f"Current conditions: {reading[1]}°C, {reading[2]}% humidity, {reading[3]} hPa"

    station = WeatherStation()
    display_1 = MockDisplay()
    display_2 = MockDisplay()
    station.attach_display(display_1)
    station.attach_display(display_2)

    station.record_reading(1622547800, 25.0, 60.0, 1013.2)
    assert display_1.last_update == "Current conditions: 25.0°C, 60.0% humidity, 1013.2 hPa"
    assert display_2.last_update == "Current conditions: 25.0°C, 60.0% humidity, 1013.2 hPa"

    station.record_reading(1622547801, 30.0, 65.0, 1015.0)
    assert display_1.last_update == "Current conditions: 30.0°C, 65.0% humidity, 1015.0 hPa"
    assert display_2.last_update == "Current conditions: 30.0°C, 65.0% humidity, 1015.0 hPa"

    station.detach_display(display_1)
    station.record_reading(1622547802, 20.0, 70.0, 1010.0)
    assert display_1.last_update == "Current conditions: 30.0°C, 65.0% humidity, 1015.0 hPa"  # No update after detaching
    assert display_2.last_update == "Current conditions: 20.0°C, 70.0% humidity, 1010.0 hPa"  # Should update

    station.detach_display(display_2)  # Detach the second display
    station.record_reading(1622547803, 22.0, 75.0, 1005.0)
    assert display_2.last_update == "Current conditions: 20.0°C, 70.0% humidity, 1010.0 hPa"  # No update after detaching

def test_raise_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(low=15.0, high=25.0)

    alerts = []
    station.alert_storage = alerts  # Assume we save alerts in a list for testing

    station.record_reading(1622547800, 26.0, 60.0, 1013.2)
    assert alerts == ["ALERT: temperature 26.0°C above threshold 25.0°C"]

    station.record_reading(1622547801, 14.0, 65.0, 1015.0)
    assert alerts == [
        "ALERT: temperature 26.0°C above threshold 25.0°C",
        "ALERT: temperature 14.0°C below threshold 15.0°C"
    ]

    station.record_reading(1622547802, 25.0, 70.0, 1010.0)
    assert alerts == [
        "ALERT: temperature 26.0°C above threshold 25.0°C",
        "ALERT: temperature 14.0°C below threshold 15.0°C"
    ]  # No alert for exactly on threshold

    # Add a test for exactly at the low threshold
    station.record_reading(1622547803, 15.0, 75.0, 1005.0)
    assert alerts == [
        "ALERT: temperature 26.0°C above threshold 25.0°C",
        "ALERT: temperature 14.0°C below threshold 15.0°C"
    ]  # No alert for exactly at the low threshold