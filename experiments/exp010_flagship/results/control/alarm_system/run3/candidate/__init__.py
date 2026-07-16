class LoudAlarm:
    def trigger(self):
        return "LOUD ALARM!"

class DayNightSwitchedAlarm:
    def __init__(self, alarm, is_day):
        self.alarm = alarm
        self.is_day = is_day

    def trigger(self):
        return self.alarm.trigger() if self.is_day else ""

class HybridAlarm:
    def __init__(self, alarms):
        self.alarms = alarms

    def trigger(self):
        return ' '.join(alarm.trigger() for alarm in self.alarms)