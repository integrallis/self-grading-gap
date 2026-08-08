# test_weather_station.py

import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()
    
    # AC-1.1: Humidity must be between 0 and 100
    station.record_reading(1620000000, 25.0, 0.0, 1013.0)  # valid humidity
    station.record_reading(1620000060, 25.0, 100.0, 1013.0)  # valid humidity
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1620000120, 25.0, -1.0, 1013.0)  # invalid humidity
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1620000180, 25.0, 101.0, 1013.0)  # invalid humidity

    # AC-1.2: Pressure must be positive
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1620000240, 25.0, 50.0, 0.0)  # invalid pressure
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1620000300, 25.0, 50.0, -1.0)  # invalid pressure

    # AC-1.3: Record valid reading
    station.record_reading(1620000360, 25.0, 50.0, 1013.0)  # valid reading
    assert station.current_reading == (1620000360, 25.0, 50.0, 1013.0)

    # AC-1.4: Before any readings
    station_no_readings = WeatherStation()
    assert station_no_readings.current_reading is None

    # AC-1.3: Multiple readings with order
    station.record_reading(1620000420, 26.0, 50.0, 1013.0)
    assert station.current_reading == (1620000420, 26.0, 50.0, 1013.0)


def test_temperature_statistics():
    station = WeatherStation()
    # AC-2.4: No readings recorded
    with pytest.raises(Exception, match="no readings recorded"):
        station.temperature_statistics()

    # Record some readings
    station.record_reading(1620000000, 20.0, 50.0, 1013.0)
    station.record_reading(1620000060, 22.0, 50.0, 1013.0)
    station.record_reading(1620000120, 24.0, 50.0, 1013.0)

    # AC-2.1: Statistics for all readings
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 20.0  # min of 20.0, 22.0, 24.0
    assert max_temp == 24.0  # max of 20.0, 22.0, 24.0
    assert avg_temp == (20.0 + 22.0 + 24.0) / 3  # average

    # AC-2.2: Statistics over a window
    min_temp_window, max_temp_window, avg_temp_window = station.temperature_statistics(1620000000, 1620000060)
    assert min_temp_window == 20.0  # only 20.0 and 22.0 in window
    assert max_temp_window == 22.0  # only 20.0 and 22.0 in window
    assert avg_temp_window == (20.0 + 22.0) / 2  # average of 20.0 and 22.0

    # AC-2.2: Statistics over a window with only end bound
    min_temp_end_only, max_temp_end_only, avg_temp_end_only = station.temperature_statistics(end=1620000120)
    assert min_temp_end_only == 20.0  # only 20.0, 22.0, and 24.0 in window
    assert max_temp_end_only == 24.0  # only 20.0, 22.0, and 24.0 in window
    assert avg_temp_end_only == (20.0 + 22.0 + 24.0) / 3  # average

    # AC-2.2: Statistics over a window with only start bound
    min_temp_start_only, max_temp_start_only, avg_temp_start_only = station.temperature_statistics(start=1620000060)
    assert min_temp_start_only == 22.0  # only 22.0 and 24.0 in window
    assert max_temp_start_only == 24.0  # only 22.0 and 24.0 in window
    assert avg_temp_start_only == (22.0 + 24.0) / 2  # average of 22.0 and 24.0

    # AC-2.4: Statistics with no readings in window
    with pytest.raises(Exception, match="no readings recorded"):
        station.temperature_statistics(start=1620000240, end=1620000300)


def test_temperature_trend():
    station = WeatherStation()
    assert station.temperature_trend() == "steady"  # AC-3.5: No readings

    # Record readings
    station.record_reading(1620000000, 20.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # AC-3.5: One reading

    station.record_reading(1620000060, 22.0, 50.0, 1013.0)
    assert station.temperature_trend() == "rising"  # AC-3.2: Rising trend

    # Test falling trend with exactly two readings
    station.record_reading(1620000120, 21.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # AC-3.4: Steady trend (22.0, 21.0)

    # Test falling trend
    station.record_reading(1620000180, 19.0, 50.0, 1013.0)
    assert station.temperature_trend() == "falling"  # AC-3.3: Falling trend

    # Test repeated temperatures
    station.record_reading(1620000240, 19.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # AC-3.4: Steady trend (19.0, 19.0)

    # Test a zig-zag trend ending above
    station.record_reading(1620000300, 20.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # AC-3.4: Steady trend (19.0, 20.0)

    # Test a zig-zag trend ending below
    station.record_reading(1620000360, 18.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # AC-3.4: Steady trend (20.0, 18.0)

    # Test a falling trend with exactly two readings
    station.record_reading(1620000420, 17.0, 50.0, 1013.0)
    assert station.temperature_trend() == "falling"  # AC-3.3: Falling trend


def test_notify_attached_displays():
    station = WeatherStation()
    # AC-4.3: No data initially
    assert station.current_conditions_display() == "No data"
    assert station.statistics_display() == "No data"

    # Attach devices
    station.attach_display("current_conditions")
    station.attach_display("statistics")

    # Record a reading
    station.record_reading(1620000000, 25.0, 50.0, 1013.0)

    # AC-4.1: Devices notified
    assert station.current_conditions_display() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"
    assert station.statistics_display() == "Temperature min 25.0°C, max 25.0°C, avg 25.0°C"

    # Record another reading
    station.record_reading(1620000060, 26.0, 50.0, 1013.0)
    assert station.current_conditions_display() == "Current conditions: 26.0°C, 50.0% humidity, 1013.0 hPa"
    assert station.statistics_display() == "Temperature min 25.0°C, max 26.0°C, avg 25.5°C"

    # Detach the current conditions display
    station.detach_display("current_conditions")
    station.record_reading(1620000120, 27.0, 50.0, 1013.0)
    assert station.current_conditions_display() == "Current conditions: 26.0°C, 50.0% humidity, 1013.0 hPa"  # No update to detached display
    assert station.statistics_display() == "Temperature min 25.0°C, max 27.0°C, avg 26.0°C"  # Updated statistics display

    # Detach a device that was never attached
    station.detach_display("non_existing_display")  # Should silently ignore
    assert station.current_conditions_display() == "Current conditions: 26.0°C, 50.0% humidity, 1013.0 hPa"


def test_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(15.0, 30.0)  # AC-5.1 and AC-5.2

    # AC-5.3: No alert at threshold
    station.record_reading(1620000000, 15.0, 50.0, 1013.0)
    assert station.alerts == []  # no alert

    station.record_reading(1620000060, 31.0, 50.0, 1013.0)
    assert station.alerts == ["ALERT: temperature 31.0°C above threshold 30.0°C"]  # AC-5.1

    station.record_reading(1620000120, 14.0, 50.0, 1013.0)
    assert station.alerts == ["ALERT: temperature 31.0°C above threshold 30.0°C", 
                               "ALERT: temperature 14.0°C below threshold 15.0°C"]  # AC-5.2

    # AC-5.3: No alert at exactly at high threshold
    station.record_reading(1620000180, 30.0, 50.0, 1013.0)
    assert station.alerts == ["ALERT: temperature 31.0°C above threshold 30.0°C", 
                               "ALERT: temperature 14.0°C below threshold 15.0°C"]  # no new alert