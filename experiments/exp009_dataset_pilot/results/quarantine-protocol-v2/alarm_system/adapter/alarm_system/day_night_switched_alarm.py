# file: alarm_system/day_night_switched_alarm.py
from candidate.impl import DayNightSwitchedAlarm as _DayNightSwitchedAlarm

class DayNightSwitchedAlarm:
    def __init__(self, wrapped_alarm, is_day):
        self._alarm = _DayNightSwitchedAlarm(wrapped_alarm, is_day)

    def trigger(self):
        return self._alarm.trigger()
