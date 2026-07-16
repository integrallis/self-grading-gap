class WeatherStation:
    def __init__(self):
        self.readings = []
        self.alerts = []
        self.temperature_thresholds = (None, None)
        self.displays = []

    def record_reading(self, timestamp, temperature, humidity, pressure):
        if not (0 <= humidity <= 100):
            raise ValueError("humidity must be between 0 and 100")
        if pressure <= 0:
            raise ValueError("pressure must be positive")
        self.readings.append((timestamp, temperature, humidity, pressure))
        self.notify_displays()
        self.check_alerts(temperature)

    def get_current_reading(self):
        return self.readings[-1][1:] if self.readings else None

    def get_temperature_statistics(self, start=None, end=None):
        if not self.readings:
            raise ValueError("no readings recorded")
        filtered_readings = [r[1] for r in self.readings if (start is None or r[0] >= start) and (end is None or r[0] <= end)]
        if not filtered_readings:
            raise ValueError("no readings recorded")
        min_temp = min(filtered_readings)
        max_temp = max(filtered_readings)
        avg_temp = sum(filtered_readings) / len(filtered_readings)
        return min_temp, max_temp, avg_temp

    def get_temperature_trend(self):
        if not self.readings:
            return "steady"
        temps = [r[1] for r in self.readings]
        if all(temps[i] < temps[i+1] for i in range(len(temps)-1)):
            return "rising"
        elif all(temps[i] > temps[i+1] for i in range(len(temps)-1)):
            return "falling"
        else:
            return "steady"

    def attach_display(self, display_type):
        display = Display(display_type, self)
        self.displays.append(display)
        display.update(self.get_current_reading())
        return display

    def set_temperature_thresholds(self, low, high):
        self.temperature_thresholds = (low, high)

    def get_alerts(self):
        return self.alerts

    def notify_displays(self):
        for display in self.displays:
            display.update(self.get_current_reading())

    def check_alerts(self, temperature):
        low, high = self.temperature_thresholds
        if low is not None and temperature < low:
            self.alerts.append(f"ALERT: temperature {temperature}°C below threshold {low}°C")
        if high is not None and temperature > high:
            self.alerts.append(f"ALERT: temperature {temperature}°C above threshold {high}°C")


class Display:
    def __init__(self, display_type, weather_station):
        self.display_type = display_type
        self.weather_station = weather_station
        self.current_reading = None

    def update(self, reading):
        if reading:
            temp, humidity, pressure = reading
            if self.display_type == "current":
                self.current_reading = f"Current conditions: {temp}°C, {humidity}% humidity, {pressure} hPa"
            elif self.display_type == "statistics":
                min_temp, max_temp, avg_temp = self.weather_station.get_temperature_statistics()
                self.current_reading = f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"
        else:
            self.current_reading = "No data"

    def get_display(self):
        return self.current_reading