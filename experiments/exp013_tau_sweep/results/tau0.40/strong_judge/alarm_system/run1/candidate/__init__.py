class LoudAlarm:
    def trigger(self):
        return "LOUD ALARM!"

class DayNightSwitchedAlarm:
    def __init__(self, alarm, is_day):
        self.alarm = alarm
        self.is_day = is_day

    def trigger(self):
        if self.is_day:
            return self.alarm.trigger()
        return ""

class HybridAlarm:
    def __init__(self, alarms):
        self.alarms = alarms

    def trigger(self):
        sounds = [alarm.trigger() for alarm in self.alarms]
        return " ".join(sounds)