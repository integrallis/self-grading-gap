class WeatherStation:
    def __init__(self):
        self.readings = []
        self.alerts = []
        self.low_threshold = None
        self.high_threshold = None
        self.displays = []

    def record_reading(self, timestamp, temperature, humidity, pressure):
        if not (0 <= humidity <= 100):
            raise ValueError("humidity must be between 0 and 100")
        if pressure <= 0:
            raise ValueError("pressure must be positive")
        if self.readings and self.readings[-1][0] >= timestamp:
            raise ValueError("readings must be recorded in order")
        self.readings.append((timestamp, temperature, humidity, pressure))
        self.check_alerts(temperature)
        self.notify_displays()

    def current_reading(self):
        return self.readings[-1] if self.readings else None

    def temperature_statistics(self, start=None, end=None):
        if not self.readings:
            raise ValueError("no readings recorded")
        filtered_readings = [(t, temp) for (t, temp, _, _) in self.readings 
                             if (start is None or t >= start) and (end is None or t <= end)]
        if not filtered_readings:
            raise ValueError("no readings recorded in the specified window")
        temperatures = [temp for _, temp in filtered_readings]
        return (min(temperatures), max(temperatures), sum(temperatures) / len(temperatures))

    def temperature_trend(self):
        if len(self.readings) <= 1:
            return "steady"
        last_temp = self.readings[-1][1]
        second_last_temp = self.readings[-2][1]
        if last_temp > second_last_temp:
            return "rising"
        elif last_temp < second_last_temp:
            return "falling"
        else:
            return "steady"

    def attach_display(self, display_name):
        self.displays.append(display_name)

    def render_current_conditions(self):
        if not self.readings:
            return "No data"
        timestamp, temperature, humidity, pressure = self.current_reading()
        return f"Current conditions: {temperature}°C, {humidity}% humidity, {pressure} hPa"

    def render_statistics(self):
        if not self.readings:
            return "No data"
        min_temp, max_temp, avg_temp = self.temperature_statistics()
        return f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

    def set_temperature_thresholds(self, low, high):
        self.low_threshold = low
        self.high_threshold = high

    def check_alerts(self, temperature):
        if self.low_threshold is not None and temperature < self.low_threshold:
            self.alerts.append(f"ALERT: temperature {temperature}°C below threshold {self.low_threshold}°C")
        if self.high_threshold is not None and temperature > self.high_threshold:
            self.alerts.append(f"ALERT: temperature {temperature}°C above threshold {self.high_threshold}°C")

    def get_alerts(self):
        return self.alerts

    def notify_displays(self):
        for display in self.displays:
            if display == "current_conditions_display":
                self.render_current_conditions()
            elif display == "statistics_display":
                self.render_statistics()