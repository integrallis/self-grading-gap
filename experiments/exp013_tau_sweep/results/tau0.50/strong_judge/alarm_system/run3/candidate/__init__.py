class LoudAlarm:
    def trigger(self):
        return "LOUD ALARM!"

class DayNightSwitchedAlarm:
    def __init__(self, wrapped_alarm, is_day):
        self.wrapped_alarm = wrapped_alarm
        self.is_day = is_day

    def trigger(self):
        return self.wrapped_alarm.trigger() if self.is_day else ""

class HybridAlarm:
    def __init__(self, alarms):
        self.alarms = alarms

    def trigger(self):
        return ' '.join(alarm.trigger() for alarm in self.alarms if alarm.trigger())