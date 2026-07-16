class WeatherStation:
    def __init__(self):
        self.readings = []
        self.current_display = "No data"
        self.statistics_display_text = "No data"
        self.temperature_thresholds = None

    def record_reading(self, timestamp, temperature, humidity, pressure):
        if not (0 <= humidity <= 100):
            raise ValueError("humidity must be between 0 and 100")
        if pressure <= 0:
            raise ValueError("pressure must be positive")
        self.readings.append((timestamp, temperature, humidity, pressure))
        self.current_display = f"Current conditions: {temperature}°C, {humidity}% humidity, {pressure} hPa"
        self.update_statistics_display()
        return self.check_alerts(temperature)

    def current_reading(self):
        if not self.readings:
            return None
        return self.readings[-1][1], self.readings[-1][2], self.readings[-1][3]

    def temperature_statistics(self, start_time=None, end_time=None):
        filtered_readings = self.filter_readings_by_time(start_time, end_time)
        if not filtered_readings:
            raise ValueError("no readings recorded")
        temperatures = [reading[1] for reading in filtered_readings]
        return min(temperatures), max(temperatures), sum(temperatures) / len(temperatures)

    def temperature_trend(self):
        if len(self.readings) < 2:
            return "steady"
        last_temp = self.readings[-1][1]
        second_last_temp = self.readings[-2][1]
        if last_temp > second_last_temp:
            return "rising"
        elif last_temp < second_last_temp:
            return "falling"
        else:
            return "steady"

    def attach_display(self, display_type):
        if display_type == "current":
            self.current_display = self.current_reading() if self.readings else "No data"
        elif display_type == "statistics":
            self.statistics_display_text = self.statistics_display() if self.readings else "No data"

    def statistics_display(self):
        if not self.readings:
            return "No data"
        min_temp, max_temp, avg_temp = self.temperature_statistics()
        return f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

    def set_temperature_thresholds(self, low, high):
        self.temperature_thresholds = (low, high)

    def check_alerts(self, temperature):
        alerts = []
        if self.temperature_thresholds:
            low, high = self.temperature_thresholds
            if temperature < low:
                alerts.append(f"ALERT: temperature {temperature}°C below threshold {low}°C")
            elif temperature > high:
                alerts.append(f"ALERT: temperature {temperature}°C above threshold {high}°C")
        return alerts

    def filter_readings_by_time(self, start_time, end_time):
        return [reading for reading in self.readings if (start_time is None or reading[0] >= start_time) and (end_time is None or reading[0] <= end_time)]

    def update_statistics_display(self):
        if not self.readings:
            self.statistics_display_text = "No data"
            return
        min_temp, max_temp, avg_temp = self.temperature_statistics()
        self.statistics_display_text = f"Temperature min {min_temp}°C, max {max_temp}°C, avg {avg_temp}°C"

    def current_conditions_display(self):
        return self.current_display