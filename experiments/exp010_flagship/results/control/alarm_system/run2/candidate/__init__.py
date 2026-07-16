class LoudAlarm:
    def trigger(self):
        return "LOUD ALARM!"

class DayNightAlarm:
    def __init__(self, wrapped_alarm, is_day):
        self.wrapped_alarm = wrapped_alarm
        self.is_day = is_day

    def trigger(self):
        if self.is_day:
            return self.wrapped_alarm.trigger()
        else:
            return ""

class HybridAlarm:
    def __init__(self, alarms):
        self.alarms = alarms

    def trigger(self):
        sounds = [alarm.trigger() for alarm in self.alarms]
        return " ".join(sounds)