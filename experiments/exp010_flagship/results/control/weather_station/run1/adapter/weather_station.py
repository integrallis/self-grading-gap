# file: weather_station.py
from candidate import WeatherStation as _WeatherStation


class Reading:
    def __init__(self, timestamp, temperature, humidity, pressure):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure


class WeatherStation(_WeatherStation):
    def record(self, reading):
        return self.record_reading(
            reading.timestamp,
            reading.temperature,
            reading.humidity,
            reading.pressure,
        )

    def add_observer(self, observer):
        observer.attach(self)
        return self.attach_display(observer.name)

    def remove_observer(self, observer):
        return observer.detach()

    def min_temperature(self, start=None, end=None):
        minimum, maximum, average = self.temperature_statistics(start, end)
        return minimum

    def max_temperature(self, start=None, end=None):
        minimum, maximum, average = self.temperature_statistics(start, end)
        return maximum

    def average_temperature(self, start=None, end=None):
        minimum, maximum, average = self.temperature_statistics(start, end)
        return average


class CurrentConditionsDisplay:
    name = "current_conditions_display"

    def __init__(self):
        self.station = None

    def attach(self, station):
        self.station = station

    def detach(self):
        self.station = None

    def render(self):
        return self.station.render_current_conditions()


class StatisticsDisplay:
    name = "statistics_display"

    def __init__(self):
        self.station = None

    def attach(self, station):
        self.station = station

    def detach(self):
        self.station = None

    def render(self):
        return self.station.render_statistics()


class TemperatureAlert:
    name = "temperature_alert"

    def __init__(self, low, high=None):
        self.low = low
        self.high = high
        self.station = None

    def attach(self, station):
        self.station = station
        return station.set_temperature_thresholds(self.low, self.high)

    def detach(self):
        self.station = None

    def raises(self, station, temperature):
        return station.check_alerts(temperature)
