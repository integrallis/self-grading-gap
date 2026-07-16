# test_weather_station.py

from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()
    
    # Test AC-1.4: No current reading before any recording
    assert station.get_current_reading() is None  # No readings recorded

    # Test AC-1.1: Valid reading
    station.record_reading("2023-10-01T00:00:00Z", 25.0, 50.0, 1013.0)
    assert station.get_current_reading() == (25.0, 50.0, 1013.0)  # Current reading updated

    # Test AC-1.1: Invalid humidity
    try:
        station.record_reading("2023-10-01T01:00:00Z", 25.0, -1.0, 1013.0)
    except ValueError as e:
        assert "humidity must be between 0 and 100" in str(e)  # Humidity validation

    try:
        station.record_reading("2023-10-01T01:00:00Z", 25.0, 101.0, 1013.0)
    except ValueError as e:
        assert "humidity must be between 0 and 100" in str(e)  # Humidity validation

    # Test AC-1.2: Invalid pressure
    try:
        station.record_reading("2023-10-01T01:00:00Z", 25.0, 50.0, 0.0)
    except ValueError as e:
        assert "pressure must be positive" in str(e)  # Pressure validation

    try:
        station.record_reading("2023-10-01T01:00:00Z", 25.0, 50.0, -1.0)
    except ValueError as e:
        assert "pressure must be positive" in str(e)  # Pressure validation


def test_temperature_statistics():
    station = WeatherStation()
    
    # Test AC-2.4: No readings recorded
    try:
        station.get_temperature_statistics()
    except ValueError as e:
        assert "no readings recorded" in str(e)  # No readings error

    # Record some valid readings
    station.record_reading("2023-10-01T00:00:00Z", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T01:00:00Z", 25.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T02:00:00Z", 30.0, 50.0, 1013.0)

    # Test AC-2.1: Statistics over all readings
    min_temp, max_temp, avg_temp = station.get_temperature_statistics()
    assert min_temp == 20.0  # Minimum temperature
    assert max_temp == 30.0  # Maximum temperature
    assert avg_temp == 25.0  # Average temperature

    # Test AC-2.2: Statistics with a time window
    start = "2023-10-01T00:00:00Z"
    end = "2023-10-01T01:00:00Z"
    min_temp, max_temp, avg_temp = station.get_temperature_statistics(start, end)
    assert min_temp == 20.0  # Minimum temperature in window
    assert max_temp == 25.0  # Maximum temperature in window
    assert avg_temp == 22.5  # Average temperature in window

    # Test AC-2.3: Statistics with a time window excluding readings
    start = "2023-10-01T02:00:00Z"
    end = "2023-10-01T02:00:01Z"
    try:
        station.get_temperature_statistics(start, end)
    except ValueError as e:
        assert "no readings recorded" in str(e)  # No readings in window error

    
def test_short_term_temperature_trend():
    station = WeatherStation()

    # Test AC-3.5: Trend with zero readings
    assert station.get_temperature_trend() == "steady"  # No readings means steady

    # Record some valid readings
    station.record_reading("2023-10-01T00:00:00Z", 20.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T01:00:00Z", 25.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T02:00:00Z", 30.0, 50.0, 1013.0)

    # Test AC-3.2: Trend is rising
    assert station.get_temperature_trend() == "rising"  # Strictly increasing

    station.record_reading("2023-10-01T03:00:00Z", 25.0, 50.0, 1013.0)  # No longer strictly increasing

    # Test AC-3.4: Trend is steady
    assert station.get_temperature_trend() == "steady"  # Not strictly increasing or decreasing


def test_notify_attached_displays():
    station = WeatherStation()

    current_display = station.attach_display("current")
    stats_display = station.attach_display("statistics")

    # Test AC-4.3: Displays show "No data" initially
    assert current_display.get_display() == "No data"  # No data at start
    assert stats_display.get_display() == "No data"  # No data at start

    # Record a valid reading
    station.record_reading("2023-10-01T00:00:00Z", 25.0, 50.0, 1013.0)

    # Test AC-4.3: Current display shows latest reading
    assert current_display.get_display() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"

    # Test AC-4.4: Statistics display shows updated statistics
    assert stats_display.get_display() == "Temperature min 25.0°C, max 25.0°C, avg 25.0°C"


def test_raise_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(15.0, 30.0)  # Low and High thresholds

    # Test AC-5.3: No alert at threshold
    station.record_reading("2023-10-01T00:00:00Z", 15.0, 50.0, 1013.0)  # At low threshold
    assert station.get_alerts() == []  # No alerts

    station.record_reading("2023-10-01T01:00:00Z", 30.0, 50.0, 1013.0)  # At high threshold
    assert station.get_alerts() == []  # No alerts

    # Test AC-5.1: Alert above high threshold
    station.record_reading("2023-10-01T02:00:00Z", 35.0, 50.0, 1013.0)  # Above threshold
    assert station.get_alerts() == ["ALERT: temperature 35.0°C above threshold 30.0°C"]

    # Test AC-5.2: Alert below low threshold
    station.record_reading("2023-10-01T03:00:00Z", 10.0, 50.0, 1013.0)  # Below threshold
    assert station.get_alerts() == [
        "ALERT: temperature 35.0°C above threshold 30.0°C",
        "ALERT: temperature 10.0°C below threshold 15.0°C"
    ]