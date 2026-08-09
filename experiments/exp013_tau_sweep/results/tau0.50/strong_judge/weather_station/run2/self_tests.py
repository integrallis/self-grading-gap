import pytest
from solution import WeatherStation

def test_record_validated_readings():
    station = WeatherStation()

    # Test 1: Valid reading
    station.record_reading(1620000000, 25.0, 50.0, 1013.0)  # timestamp, temperature, humidity, pressure
    assert station.current_reading is not None  # current reading should exist after recording
    assert station.current_reading[1] == 25.0  # temperature

    # Test 2: Valid humidity boundary 0
    station.record_reading(1620000010, 25.0, 0.0, 1013.0)  # humidity = 0
    assert station.current_reading[2] == 0.0  # humidity

    # Test 3: Valid humidity boundary 100
    station.record_reading(1620000020, 25.0, 100.0, 1013.0)  # humidity = 100
    assert station.current_reading[2] == 100.0  # humidity

    # Test 4: Invalid humidity above 100
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1620000030, 25.0, 101.0, 1013.0)

    # Test 5: Invalid humidity below 0
    with pytest.raises(Exception, match="humidity must be between 0 and 100"):
        station.record_reading(1620000040, 25.0, -1.0, 1013.0)

    # Test 6: Invalid pressure
    with pytest.raises(Exception, match="pressure must be positive"):
        station.record_reading(1620000050, 25.0, 50.0, 0)

    # Test 7: Current reading after multiple records
    station.record_reading(1620000060, 26.0, 55.0, 1013.5)
    assert station.current_reading[1] == 26.0  # temperature should be latest

    # Test 8: No current reading before any record
    station2 = WeatherStation()
    assert station2.current_reading is None


def test_temperature_statistics():
    station = WeatherStation()
    station.record_reading(1620000000, 20.0, 50.0, 1013.0)
    station.record_reading(1620000020, 25.0, 50.0, 1013.0)
    station.record_reading(1620000040, 30.0, 50.0, 1013.0)

    # Test 1: Statistics with no window
    min_temp, max_temp, avg_temp = station.temperature_statistics()
    assert min_temp == 20.0  # min of [20.0, 25.0, 30.0]
    assert max_temp == 30.0  # max of [20.0, 25.0, 30.0]
    assert avg_temp == 25.0  # avg of [20.0, 25.0, 30.0] = (20 + 25 + 30) / 3

    # Test 2: Statistics with a valid window
    min_temp, max_temp, avg_temp = station.temperature_statistics(start=1620000010, end=1620000040)
    assert min_temp == 25.0  # min of [25.0, 30.0]
    assert max_temp == 30.0  # max of [25.0, 30.0]
    assert avg_temp == 27.5  # avg of [25.0, 30.0] = (25 + 30) / 2

    # Test 3: Statistics with no valid readings
    with pytest.raises(Exception, match="no readings recorded"):
        station.temperature_statistics(start=1620000050, end=1620000060)

    # Test 4: Statistics with start-only window
    min_temp, max_temp, avg_temp = station.temperature_statistics(start=1620000000)
    assert min_temp == 20.0  # min of [20.0, 25.0, 30.0]
    assert max_temp == 30.0  # max of [20.0, 25.0, 30.0]
    assert avg_temp == 25.0  # avg of [20.0, 25.0, 30.0]

    # Test 5: Statistics with end-only window
    min_temp, max_temp, avg_temp = station.temperature_statistics(end=1620000040)
    assert min_temp == 20.0  # min of [20.0, 25.0, 30.0]
    assert max_temp == 30.0  # max of [20.0, 25.0, 30.0]
    assert avg_temp == 25.0  # avg of [20.0, 25.0, 30.0]

    # Test 6: Exclusion after end
    station.record_reading(1620000060, 35.0, 50.0, 1013.0)  # This reading should be excluded
    min_temp, max_temp, avg_temp = station.temperature_statistics(start=1620000010, end=1620000040)
    assert min_temp == 25.0  # min of [25.0, 30.0]
    assert max_temp == 30.0  # max of [25.0, 30.0]
    assert avg_temp == 27.5  # avg of [25.0, 30.0]

    # Test 7: Statistics with no readings at all
    station_empty = WeatherStation()
    with pytest.raises(Exception, match="no readings recorded"):
        station_empty.temperature_statistics()


def test_short_term_temperature_trend():
    station = WeatherStation()
    station.record_reading(1620000000, 20.0, 50.0, 1013.0)
    station.record_reading(1620000020, 25.0, 50.0, 1013.0)
    station.record_reading(1620000040, 30.0, 50.0, 1013.0)

    # Test 1: Rising trend
    assert station.temperature_trend() == "rising"

    # Test 2: Falling trend with last three readings
    station.record_reading(1620000060, 20.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"  # last 3 readings are [25.0, 30.0, 20.0]

    # Test 3: Steady trend
    station.record_reading(1620000080, 20.0, 50.0, 1013.0)
    station.record_reading(1620000100, 20.0, 50.0, 1013.0)
    assert station.temperature_trend() == "steady"

    # Test 4: Two readings rising
    station2 = WeatherStation()
    station2.record_reading(1620000000, 20.0, 50.0, 1013.0)
    station2.record_reading(1620000020, 25.0, 50.0, 1013.0)
    assert station2.temperature_trend() == "rising"

    # Test 5: Three readings falling
    station3 = WeatherStation()
    station3.record_reading(1620000000, 30.0, 50.0, 1013.0)
    station3.record_reading(1620000020, 25.0, 50.0, 1013.0)
    station3.record_reading(1620000040, 20.0, 50.0, 1013.0)
    assert station3.temperature_trend() == "falling"

    # Test 6: One reading
    station4 = WeatherStation()
    station4.record_reading(1620000000, 20.0, 50.0, 1013.0)
    assert station4.temperature_trend() == "steady"

    # Test 7: Zero readings
    station5 = WeatherStation()
    assert station5.temperature_trend() == "steady"

    # Test 8: Zig-zag trend ending above starting temperature
    station6 = WeatherStation()
    station6.record_reading(1620000000, 20.0, 50.0, 1013.0)
    station6.record_reading(1620000020, 25.0, 50.0, 1013.0)
    station6.record_reading(1620000040, 20.0, 50.0, 1013.0)
    assert station6.temperature_trend() == "steady"


def test_notify_attached_displays():
    station = WeatherStation()
    display1 = MockDisplay()
    display2 = MockDisplay()
    station.attach_display(display1)
    station.attach_display(display2)

    station.record_reading(1620000000, 25.0, 50.0, 1013.0)
    assert display1.notifications == ["Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"]
    assert display2.notifications == ["Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"]

    station.detach_display(display1)
    station.record_reading(1620000010, 26.0, 55.0, 1013.5)
    assert display1.notifications == ["Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa"]  # no new
    assert display2.notifications == ["Current conditions: 25.0°C, 50.0% humidity, 1013.0 hPa",
                                       "Current conditions: 26.0°C, 55.0% humidity, 1013.5 hPa"]

    # Test 1: Detaching a never-attached device silently ignored
    display3 = MockDisplay()
    station.detach_display(display3)  # should not raise any error

    # Test 2: Current conditions display before any readings
    station_empty = WeatherStation()
    assert display3.notifications == []  # no notifications sent


def test_temperature_alerts():
    station = WeatherStation()
    station.set_temperature_thresholds(low=15.0, high=25.0)

    # Test 1: Alert when above threshold
    station.record_reading(1620000000, 26.0, 50.0, 1013.0)  # This should record an alert
    assert station.alerts[-1] == "ALERT: temperature 26.0°C above threshold 25.0°C"

    # Test 2: Alert when below threshold
    station.record_reading(1620000010, 14.0, 50.0, 1013.0)  # This should record an alert
    assert station.alerts[-1] == "ALERT: temperature 14.0°C below threshold 15.0°C"

    # Test 3: No alert when exactly at threshold
    station.record_reading(1620000020, 25.0, 50.0, 1013.0)  # This should not record an alert
    assert len(station.alerts) == 2  # still only 2 alerts

    # Test 4: Exact low threshold
    station.record_reading(1620000030, 15.0, 50.0, 1013.0)  # This should not record an alert
    assert len(station.alerts) == 2  # still only 2 alerts


class MockDisplay:
    def __init__(self):
        self.notifications = []

    def notify(self, message):
        self.notifications.append(message)