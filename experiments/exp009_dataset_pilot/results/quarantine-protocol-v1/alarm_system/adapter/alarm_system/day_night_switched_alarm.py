# file: alarm_system/day_night_switched_alarm.py
from candidate.impl import DayNightSwitchedAlarm as _DayNightSwitchedAlarm

class DayNightSwitchedAlarm(_DayNightSwitchedAlarm):
    def __init__(self, wrapped_alarm, is_day):
        super().__init__(wrapped_alarm, is_day)

    def trigger(self):
        return super().trigger()
