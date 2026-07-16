# candidate/impl.py

class LoudAlarm:
    def trigger(self):
        return "LOUD ALARM!"


class DayNightSwitchedAlarm:
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
        return " ".join(sound for sound in sounds if sound)


# Example usage (should be removed in production)
if __name__ == "__main__":
    loud_alarm = LoudAlarm()
    print(loud_alarm.trigger())  # Should print "LOUD ALARM!"

    day_alarm = DayNightSwitchedAlarm(loud_alarm, is_day=True)
    print(day_alarm.trigger())  # Should print "LOUD ALARM!"

    night_alarm = DayNightSwitchedAlarm(loud_alarm, is_day=False)
    print(night_alarm.trigger())  # Should print ""

    hybrid_alarm = HybridAlarm([loud_alarm, loud_alarm])
    print(hybrid_alarm.trigger())  # Should print "LOUD ALARM! LOUD ALARM!"
