# file: weather_station.py
from datetime import datetime

from candidate import Display as _CandidateDisplay
from candidate import WeatherStation as _CandidateWeatherStation


class Reading:
    def __init__(self, timestamp, temperature, humidity, pressure):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def __iter__(self):
        return iter((
            self.timestamp,
            self.temperature,
            self.humidity,
            self.pressure,
        ))


class _DisplayObserver:
    def _bind(self, weather_station):
        self._weather_station = weather_station
        self._display = _CandidateDisplay(
            self._display_type,
            weather_station._station,
        )
        return self.update(weather_station._station.get_current_reading())

    def update(self, reading):
        return self._display.update(reading)

    def render(self):
        return self._display.get_display()


class CurrentConditionsDisplay(_DisplayObserver):
    _display_type = "current"


class StatisticsDisplay(_DisplayObserver):
    _display_type = "statistics"


class TemperatureAlert:
    def __init__(self, low, high=None):
        self.low = low
        self.high = high

    def _bind(self, weather_station):
        self._weather_station = weather_station
        return weather_station._station.set_temperature_thresholds(
            self.low,
            self.high,
        )

    def update(self, reading):
        return None

    def raises(self, temperature, weather_station):
        weather_station._station.set_temperature_thresholds(
            self.low,
            self.high,
        )
        weather_station._station.check_alerts(temperature)
        return weather_station._station.get_alerts()


class WeatherStation:
    def __init__(self):
        self._station = _CandidateWeatherStation()

    def add_observer(self, observer):
        observer._bind(self)
        self._station.displays.append(observer)
        return observer

    def remove_observer(self, observer):
        return self._station.displays.remove(observer)

    def record(self, reading):
        return self._station.record_reading(*reading)

    def min_temperature(self, *dates):
        minimum, maximum, average = self._station.get_temperature_statistics(
            *dates,
        )
        return minimum

    def max_temperature(self, *dates):
        minimum, maximum, average = self._station.get_temperature_statistics(
            *dates,
        )
        return maximum

    def average_temperature(self, *dates):
        minimum, maximum, average = self._station.get_temperature_statistics(
            *dates,
        )
        return average

    def temperature_trend(self):
        return self._station.get_temperature_trend()
