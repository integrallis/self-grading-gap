import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()
    
    # AC-1.1: Valid reading
    station.record_reading(1633072800, 20.0, 50.0, 1013.0)  # timestamp, temp, humidity, pressure
    assert station.current_reading  # Check that there is a current reading

    # AC-1.1: Humidity boundary cases
    station.record_reading(1633072801, 21.0, 0.0, 1013.0)  # humidity exactly 0
    assert station.current_reading  # Check that there is a current reading
    
    station.record_reading(1633072802, 22.0, 100.0, 1013.0)  # humidity exactly 100
    assert station.current_reading  # Check that there is a current reading

    # AC-1.1: Invalid humidity
    with pytest.raises(Exception) as excinfo:
        station.record_reading(1633072803, 23.0, -1.0, 1013.0)
    assert "humidity must be between 0 and 100" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        station.record_reading(1633072804, 24.0, 101.0, 1013.0)
    assert "humidity must be between 0 and 100" in str(excinfo.value)

    # AC-1.2: Invalid pressure
    with pytest.raises(Exception) as excinfo:
        station.record_reading(1633072805, 25.0, 50.0, 0.0)
    assert "pressure must be positive" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        station.record_reading(1633072806, 26.0, 50.0, -1.0)
    assert "pressure must be positive" in str(excinfo.value)

    # AC-1.3: Ensure readings are in order (not a tuple check, just verify order)
    assert station.current_reading  # Check that there is a current reading

    # AC-1.4: No current reading before any record
    station_empty = WeatherStation()
    assert station_empty.current_reading is None


def test_temperature_statistics():
    station = WeatherStation()
    # Add readings
    station.record_reading(1633072800, 20.0, 50.0, 1013.0)
    station.record_reading(1633072801, 22.0, 50.0, 1013.0)
    station.record_reading(1633072802, 21.0, 50.0, 1013.0)
    station.record_reading(1633072803, 23.0, 50.0, 1013.0)
    
    # AC-2.1: Statistics over all readings
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 20.0  # min value of (20.0, 22.0, 21.0, 23.0)
    assert max_temp == 23.0  # max value of (20.0, 22.0, 21.0, 23.0)
    assert avg_temp == 21.5  # average (20.0 + 22.0 + 21.0 + 23.0) / 4 = 21.5

    # AC-2.2: Windowed statistics with inclusive bounds
    min_temp_window, max_temp_window, avg_temp_window = station.temperature_statistics(start=1633072801, end=1633072803)
    assert min_temp_window == 21.0  # min value of (22.0, 21.0, 23.0)
    assert max_temp_window == 23.0  # max value of (22.0, 21.0, 23.0)
    assert avg_temp_window == 22.0  # average (22.0 + 21.0 + 23.0) / 3 = 22.0

    # AC-2.2: Start-only statistics
    min_temp_start, max_temp_start, avg_temp_start = station.temperature_statistics(start=1633072801)
    assert min_temp_start == 21.0  # min value of (22.0, 21.0, 23.0)
    assert max_temp_start == 23.0  # max value of (22.0, 21.0, 23.0)
    assert avg_temp_start == 22.0  # average (22.0 + 21.0 + 23.0) / 3 = 22.0

    # AC-2.2: End-only statistics
    min_temp_end, max_temp_end, avg_temp_end = station.temperature_statistics(end=1633072802)
    assert min_temp_end == 20.0  # min value of (20.0, 22.0, 21.0)
    assert max_temp_end == 22.0  # max value of (20.0, 22.0, 21.0)
    assert avg_temp_end == 20.5  # average (20.0 + 22.0) / 2 = 21.0

    # AC-2.4: No readings recorded error
    station_empty = WeatherStation()
    with pytest.raises(Exception) as excinfo:
        station_empty.temperature_statistics()
    assert "no readings recorded" in str(excinfo.value)

    # AC-2.4: No readings in window
    with pytest.raises(Exception) as excinfo:
        station.temperature_statistics(start=1633072810, end=1633072899)  # No readings in this window
    assert "no readings recorded" in str(excinfo.value)

    # AC-2.3: Exclusion after an end bound
    station.record_reading(1633072900, 25.0, 50.0, 1013.0)
    min_temp_after_end, max_temp_after_end, avg_temp_after_end = station.temperature_statistics(start=1633072801, end=1633072802)
    assert min_temp_after_end == 21.0  # min value of (22.0, 21.0)
    assert max_temp_after_end == 22.0  # max value of (22.0, 21.0)
    assert avg_temp_after_end == 21.0  # average (22.0 + 21.0) / 2 = 21.0


def test_short_term_temperature_trend():
    station = WeatherStation()
    # Add readings
    station.record_reading(1633072800, 20.0, 50.0, 1013.0)
    station.record_reading(1633072801, 21.0, 50.0, 1013.0)
    station.record_reading(1633072802, 22.0, 50.0, 1013.0)

    # AC-3.2: Trend is rising
    trend = station.temperature_trend()
    assert trend == "rising"

    # Add a reading that decreases
    station.record_reading(1633072803, 21.0, 50.0, 1013.0)
    trend = station.temperature_trend()
    assert trend == "steady"

    # AC-3.5: With zero reading
    station_empty = WeatherStation()
    trend_empty = station_empty.temperature_trend()
    assert trend_empty == "steady"

    # AC-3.5: With one reading
    station.record_reading(1633072900, 15.0, 50.0, 1013.0)
    trend_one = station.temperature_trend()
    assert trend_one == "steady"

    # AC-3.1: Trend considers only the three most recent readings
    station.record_reading(1633072901, 16.0, 50.0, 1013.0)
    station.record_reading(1633072902, 17.0, 50.0, 1013.0)
    station.record_reading(1633072903, 18.0, 50.0, 1013.0)
    trend_recent = station.temperature_trend()
    assert trend_recent == "rising"

    # AC-3.2: Trend is rising with exactly two readings
    station.record_reading(1633072904, 19.0, 50.0, 1013.0)  # Adding a reading to keep the last two
    trend_two_rising = station.temperature_trend()
    assert trend_two_rising == "rising"

    # AC-3.3: Trend is falling with exactly two readings
    station.record_reading(1633072905, 17.0, 50.0, 1013.0)  # Adding a reading to make it falling
    trend_two_falling = station.temperature_trend()
    assert trend_two_falling == "falling"

    # AC-3.4: Repeated temperature
    station.record_reading(1633072906, 17.0, 50.0, 1013.0)  # Repeated temperature
    trend_repeated = station.temperature_trend()
    assert trend_repeated == "steady"


def test_notify_attached_displays():
    class DisplayDevice:
        def __init__(self):
            self.last_message = "No data"

        def update_current(self, temperature, humidity, pressure):
            self.last_message = f"Current conditions: {temperature}°C, {humidity}% humidity, {pressure} hPa"

        def update_statistics(self, min_temp, max_temp, avg_temp):
            self.last_message = f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

    station = WeatherStation()
    display_current = DisplayDevice()
    display_statistics = DisplayDevice()
    
    station.attach(display_current)
    station.attach(display_statistics)

    # AC-4.1: Notify attached devices
    station.record_reading(1633072800, 20.0, 50.0, 1013.0)
    assert display_current.last_message == "Current conditions: 20.0°C, 50.0% humidity, 1013.0 hPa"
    assert display_statistics.last_message == "Temperature min 20.0°C, max 20.0°C, avg 20.0°C"

    # AC-4.1: Notify attached devices with second reading
    station.record_reading(1633072801, 21.0, 50.0, 1013.0)
    assert display_current.last_message == "Current conditions: 21.0°C, 50.0% humidity, 1013.0 hPa"
    assert display_statistics.last_message == "Temperature min 20.0°C, max 21.0°C, avg 20.5°C"

    # AC-4.2: Detach a device
    station.detach(display_current)
    station.record_reading(1633072802, 22.0, 50.0, 1013.0)
    assert display_statistics.last_message == "Temperature min 20.0°C, max 22.0°C, avg 20.666666666666668"  # avg updated

    # AC-4.2: Detach a device that was never attached
    station.detach(display_current)  # Silent ignore

    # AC-4.2: Verify detached device does not receive updates
    station.record_reading(1633072803, 23.0, 50.0, 1013.0)
    assert display_current.last_message == "Current conditions: 21.0°C, 50.0% humidity, 1013.0 hPa"  # Should remain unchanged

    # AC-4.3: Verify "No data" before any reading
    new_station = WeatherStation()
    assert display_current.last_message == "No data"
    assert display_statistics.last_message == "No data"


def test_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(low=15.0, high=25.0)

    # AC-5.1: Above threshold alert
    station.record_reading(1633072800, 26.0, 50.0, 1013.0)  # Should trigger alert
    assert "ALERT: temperature 26.0°C above threshold 25.0°C" in str(station.alerts)
    
    # AC-5.2: Below threshold alert
    station.record_reading(1633072801, 14.0, 50.0, 1013.0)  # Should trigger alert
    assert "ALERT: temperature 14.0°C below threshold 15.0°C" in str(station.alerts)

    # AC-5.3: Exactly at threshold
    station.record_reading(1633072802, 25.0, 50.0, 1013.0)  # No alert should be raised
    assert "ALERT: temperature 25.0°C above threshold 25.0°C" not in str(station.alerts)
    assert "ALERT: temperature 25.0°C below threshold 15.0°C" not in str(station.alerts)