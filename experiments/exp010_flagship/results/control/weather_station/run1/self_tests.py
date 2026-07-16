# test_weather_station.py

from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()

    # AC-1.4: Before anything has been recorded there is no current reading.
    assert station.current_reading() is None

    # AC-1.1: Valid reading
    station.record_reading(1625239200, 25.0, 50.0, 1013.0)  # timestamp, temperature, humidity, pressure
    assert station.current_reading() == (1625239200, 25.0, 50.0, 1013.0)

    # AC-1.1: Humidity must be between 0 and 100 inclusive
    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading(1625239260, 25.0, -1.0, 1013.0)

    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        station.record_reading(1625239320, 25.0, 101.0, 1013.0)

    # AC-1.2: Pressure must be positive
    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading(1625239380, 25.0, 50.0, 0.0)

    with pytest.raises(ValueError, match="pressure must be positive"):
        station.record_reading(1625239440, 25.0, 50.0, -1.0)

    # AC-1.3: Keep readings in order
    station.record_reading(1625239500, 20.0, 50.0, 1013.0)
    assert station.current_reading() == (1625239500, 20.0, 50.0, 1013.0)

def test_temperature_statistics():
    station = WeatherStation()
    
    # AC-2.4: Asking for statistics when no readings qualify is an error
    with pytest.raises(ValueError, match="no readings recorded"):
        station.temperature_statistics()

    # Adding readings
    station.record_reading(1625239200, 25.0, 50.0, 1013.0)
    station.record_reading(1625239260, 30.0, 50.0, 1013.0)
    station.record_reading(1625239320, 20.0, 50.0, 1013.0)

    # AC-2.1: Minimum, maximum, and average temperature
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 20.0  # min of [25.0, 30.0, 20.0]
    assert max_temp == 30.0  # max of [25.0, 30.0, 20.0]
    assert avg_temp == 25.0  # avg of [25.0, 30.0, 20.0] = (25+30+20)/3

    # AC-2.2: Windowed statistics
    min_temp, max_temp, avg_temp = station.temperature_statistics(start=1625239200, end=1625239260)
    assert min_temp == 25.0  # min of [25.0, 30.0]
    assert max_temp == 30.0  # max of [25.0, 30.0]
    assert avg_temp == 27.5  # avg of [25.0, 30.0] = (25+30)/2

def test_temperature_trend():
    station = WeatherStation()

    # AC-3.5: With zero or one reading the trend is "steady"
    assert station.temperature_trend() == "steady"

    # Adding readings
    station.record_reading(1625239200, 25.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"

    station.record_reading(1625239260, 30.0, 50.0, 1013.0)
    assert station.temperature_trend() == "rising"  # 25.0 to 30.0 is rising

    station.record_reading(1625239320, 20.0, 50.0, 1013.0)
    assert station.temperature_trend() == "falling"  # 30.0 to 20.0 is falling

    station.record_reading(1625239380, 20.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # 20.0 to 20.0 is steady

def test_notify_attached_displays():
    station = WeatherStation()
    station.attach_display("current_conditions_display")
    station.attach_display("statistics_display")

    # AC-4.3: No data before any reading
    assert station.render_current_conditions() == "No data"
    assert station.render_statistics() == "No data"

    # Recording a reading
    station.record_reading(1625239200, 25.0, 50.0, 1013.0)

    # AC-4.1: Displays should be notified
    assert station.render_current_conditions() == "Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"
    assert station.render_statistics() == "Temperature min 25.0°C, max 25.0°C, avg 25.0°C"

def test_raise_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(low=15.0, high=30.0)

    # AC-5.3: A reading exactly at a threshold raises no alert
    station.record_reading(1625239200, 15.0, 50.0, 1013.0)
    assert station.get_alerts() == []

    station.record_reading(1625239260, 31.0, 50.0, 1013.0)
    assert station.get_alerts() == ["ALERT: temperature 31.0°C above threshold 30.0°C"]

    station.record_reading(1625239320, 14.0, 50.0, 1013.0)
    assert station.get_alerts() == ["ALERT: temperature 31.0°C above threshold 30.0°C", 
                                     "ALERT: temperature 14.0°C below threshold 15.0°C"]