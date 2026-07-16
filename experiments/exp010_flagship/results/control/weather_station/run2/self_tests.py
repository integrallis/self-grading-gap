from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()

    # AC-1.4: Before anything has been recorded there is no current reading.
    assert station.current_reading() is None
    
    # AC-1.1: Valid reading
    station.record_reading("2023-10-01T12:00:00Z", 25.0, 50.0, 1013.0)
    assert station.current_reading() == (25.0, 50.0, 1013.0)

    # AC-1.1: Invalid humidity
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading("2023-10-01T12:01:00Z", 25.0, -1.0, 1013.0)
    
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading("2023-10-01T12:02:00Z", 25.0, 101.0, 1013.0)

    # AC-1.2: Invalid pressure
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading("2023-10-01T12:03:00Z", 25.0, 50.0, 0)
    
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading("2023-10-01T12:04:00Z", 25.0, 50.0, -1)

    # AC-1.3: Keep readings in order and report current reading
    station.record_reading("2023-10-01T12:05:00Z", 20.0, 55.0, 1015.0)
    assert station.current_reading() == (20.0, 55.0, 1015.0)

def test_temperature_statistics_over_time_window():
    station = WeatherStation()
    
    # AC-2.4: Asking for statistics when no readings qualify
    with pytest.raises(ValueError, match="no readings recorded"):
        station.temperature_statistics()

    # Valid readings
    station.record_reading("2023-10-01T12:00:00Z", 25.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:01:00Z", 30.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:02:00Z", 20.0, 50.0, 1013.0)

    # AC-2.1: Minimum, maximum, and average temperature cover all readings
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 20.0  # (25.0, 30.0, 20.0) -> min = 20.0
    assert max_temp == 30.0  # (25.0, 30.0, 20.0) -> max = 30.0
    assert avg_temp == 25.0  # (25.0 + 30.0 + 20.0) / 3 = 25.0

    # AC-2.2: A window may bound the statistics
    start_time = "2023-10-01T12:00:00Z"
    end_time = "2023-10-01T12:01:00Z"
    min_temp, max_temp, avg_temp = station.temperature_statistics(start_time, end_time)
    assert min_temp == 25.0  # Only includes 25.0 and 30.0
    assert max_temp == 30.0  
    assert avg_temp == 27.5  # (25.0 + 30.0) / 2 = 27.5

    # AC-2.3: Readings before the window's start are excluded
    start_time = "2023-10-01T12:01:00Z"
    end_time = "2023-10-01T12:02:00Z"
    min_temp, max_temp, avg_temp = station.temperature_statistics(start_time, end_time)
    assert min_temp == 30.0  # Only includes 30.0 and 20.0
    assert max_temp == 30.0  
    assert avg_temp == 25.0  # (30.0 + 20.0) / 2 = 25.0

def test_short_term_temperature_trend():
    station = WeatherStation()

    # AC-3.5: With zero or one reading the trend is "steady"
    assert station.temperature_trend() == "steady"

    # Valid readings
    station.record_reading("2023-10-01T12:00:00Z", 25.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"

    station.record_reading("2023-10-01T12:01:00Z", 26.0, 50.0, 1013.0)
    assert station.temperature_trend() == "rising"  # 25.0 -> 26.0 is rising

    station.record_reading("2023-10-01T12:02:00Z", 27.0, 50.0, 1013.0)
    assert station.temperature_trend() == "rising"  # 26.0 -> 27.0 is rising

    station.record_reading("2023-10-01T12:03:00Z", 26.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # 27.0 -> 26.0 is not rising

    station.record_reading("2023-10-01T12:04:00Z", 25.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # 26.0 -> 25.0 is not rising

def test_notify_attached_displays():
    station = WeatherStation()
    
    # AC-4.3: Current conditions display shows "No data" before it has received anything
    assert station.current_conditions_display() == "No data"
    
    # AC-4.4: Statistics display also shows "No data"
    assert station.statistics_display() == "No data"
    
    # Attach displays
    station.attach_display("current")
    station.attach_display("statistics")

    # Record a valid reading
    station.record_reading("2023-10-01T12:00:00Z", 25.0, 50.0, 1013.0)
    
    # AC-4.1: Every attached device is notified of each newly recorded reading
    assert station.current_conditions_display() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"
    assert station.statistics_display() == "Temperature min 25.0°C, max 25.0°C, avg 25.0°C"

def test_raise_temperature_alerts():
    station = WeatherStation()
    
    # Set thresholds
    station.set_temperature_thresholds(low=15.0, high=30.0)

    # AC-5.3: A reading exactly at a threshold raises no alert
    station.record_reading("2023-10-01T12:00:00Z", 15.0, 50.0, 1013.0)
    station.record_reading("2023-10-01T12:01:00Z", 30.0, 50.0, 1013.0)

    # AC-5.1: A reading strictly above the configured high threshold records an alert
    alerts = station.record_reading("2023-10-01T12:02:00Z", 31.0, 50.0, 1013.0)
    assert alerts == ["ALERT: temperature 31.0°C above threshold 30.0°C"]

    # AC-5.2: A reading strictly below the configured low threshold records an alert
    alerts = station.record_reading("2023-10-01T12:03:00Z", 14.0, 50.0, 1013.0)
    assert alerts == ["ALERT: temperature 14.0°C below threshold 15.0°C"]